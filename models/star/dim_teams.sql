with source as (
    select * from {{ ref('stg_teams') }}
)

select 
    id,
    name
from source