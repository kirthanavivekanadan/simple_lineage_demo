-- models/my_second_model.sql

select
    customer_id,
    first_name,
    last_name,
    email,
upper(FIRST_NAME || ' ' || LAST_NAME) as FULL_NAME_UPPERCASE
from {{ ref('my_first_model') }}