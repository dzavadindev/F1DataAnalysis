with drivers as (
    select * from {{ ref('stg_drivers') }}
),
driver_teams as (
    select * from {{ ref('stg_drivers_teams') }}
)

select 
    d.id,
    d.full_name,
    d.code,
from drivers d
where d.code is not null 