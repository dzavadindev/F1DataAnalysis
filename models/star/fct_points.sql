with source as (
    select * from {{ ref('stg_constructors_results') }}
)

select
    year,
    team,
    race_name,
    points
from source