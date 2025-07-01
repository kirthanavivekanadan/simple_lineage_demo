-- models/my_first_model.sql

select
    customer_id,
    first_name,
    last_name,
    email
from {{ ref('customers') }}