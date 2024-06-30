with source as (
    select * from {{ ref('int_races') }}
)

select 
    name,
    year,
    races_amount,
    first_place_points
from source