with races as (
    select *, extract(year from date) as year from {{ ref('stg_races') }}
),
races_number as (
    select * from {{ ref('stg_races_carried_out') }}
)

select 
    r.race as name,
    r.year,
    rn.races_amount,
    rn.first_place_points
from races r
left join races_number rn on r.year = rn.year