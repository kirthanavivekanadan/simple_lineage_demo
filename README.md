# DBT Failure Impact Analyzer
A Python-based utility to detect failed DBT models and trace their downstream impact using DBT's artifact files: run_results.json and manifest.json.

This tool helps you debug faster, reduce pipeline downtime, and build trust in your data pipelines.

# Why This Tool?
DBT's DAG shows the structure of your data pipeline, but it doesn't highlight runtime failures or automatically flag downstream impact when a model fails.
  -  This tool addresses that limitation by:
  -  Parsing run_results.json to detect failed models
  -  Reading manifest.json to understand dependency relationships
  -  Traversing the graph to identify all downstream models truly impacted
  -  Producing a clear, machine-readable impact report

# Features
  - Detects failed models from run_results.json
  - Parses manifest.json to read the DAG structure
  - Filters out unaffected models
  - Outputs a clean report listing all impacted models

# How It Works
 - run_results.json tells us which models failed in the last dbt run.
 - manifest.json describes the model dependency graph.
 - The tool traverses the DAG to find all models depending (directly or indirectly) on the failed ones.
 - It generates a report listing failed models and all downstream models impacted.

# Example Output:
Models FAILED in last run:
  - my_model_a

All IMPACTED downstream models (including failed):
  - my_model_a (failed)
  - my_model_b
  - my_model_c

# Project Structure

dbt-failure-impact-analyzer/
│
├── target/
│   ├── manifest.json
│   └── run_results.json
│
├── lineage_breakage.py     # Main analysis script
└── README.md
