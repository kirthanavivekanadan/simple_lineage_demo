#!/usr/bin/env python3
"""
This script finds dbt models that failed during the last run,
and then finds every other model that depends on those failed models.
It prints a simple report and can create a graph file to visualize the dependencies.

Run this script with:
    python lineage_breakage.py
"""

import json
from pathlib import Path
from collections import defaultdict, deque

# Set paths to dbt output files (generated after running dbt)
TARGET_DIR = Path("target")
MANIFEST_FILE = TARGET_DIR / "manifest.json"       # Contains model definitions & dependencies
RUN_RESULTS_FILE = TARGET_DIR / "run_results.json" # Contains run status of each model

# Step 1: Load the JSON files into Python dictionaries
with MANIFEST_FILE.open() as f:
    manifest = json.load(f)

with RUN_RESULTS_FILE.open() as f:
    run_results = json.load(f)

# Get all models and other dbt resources from the manifest
nodes = manifest["nodes"]

# Step 2: Find all models that failed during the last dbt run
failed_models = set()
for result in run_results["results"]:
    if result["status"] == "error":
        failed_models.add(result["unique_id"])

# If no models failed, print a message and exit early
if not failed_models:
    print("No failed models in last run – nothing to highlight.")
    exit(0)

# Step 3: Build a map of dependencies:
# For each model, list which models depend on it (i.e., its children)
dependency_map = defaultdict(list)  # key = parent model id, value = list of child model ids

for node_id, node in nodes.items():
    # We only care about models, not seeds/tests/macros etc.
    if node["resource_type"] != "model":
        continue
    
    # 'depends_on' lists what this model depends on (its parents)
    parents = node["depends_on"]["nodes"]

    # For each parent, add this model to that parent's list of children
    for parent in parents:
        if parent.startswith("model."):  # only consider model parents
            dependency_map[parent].append(node_id)

# Step 4: Starting from the failed models, find all downstream impacted models
# Start with the models that failed
impacted_models = set(failed_models)

# Use a list as a queue to keep track of models we need to check
models_to_check = list(failed_models)

# Loop until there are no more models to check
while models_to_check:
    # Take the first model from the list
    current_model = models_to_check.pop(0)
    
    # Find models that depend on the current model (children)
    children = dependency_map.get(current_model, [])
    
    # For each child model:
    for child in children:
        # If we haven't already marked this child as impacted:
        if child not in impacted_models:
            # Add it to the impacted set
            impacted_models.add(child)
            # And add it to the list to check its children later
            models_to_check.append(child)
# Step 5: Prepare a helper function to shorten model names for printing
def short_name(full_id):
    # Example: model.project_name.model_name --> model_name
    return full_id.split(".", 2)[-1]

# Step 6: Print out the report
print("\nModels FAILED in last run:")
for failed_model in failed_models:
    print("  •", short_name(failed_model))

print("\nAll IMPACTED downstream models (including failed):")
for model in sorted(impacted_models):
    status = " (failed)" if model in failed_models else ""
    print("  •", short_name(model) + status)
