with source as (
    select * from {{ ref('int_drivers') }}
)

select 
    id,
    full_name,
    code,
    team
from source
where code is not null 