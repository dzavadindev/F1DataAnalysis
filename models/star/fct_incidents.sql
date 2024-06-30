with source as (
    select * from {{ ref('stg_incidents') }}
)

select
    date,
    driver_one_code,
    driver_two_code,
    race
from source