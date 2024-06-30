with source as (
      select * from {{ source('raw_data', 'raw_teams') }}
)

select 
    id,
    name,
    nationality as country
from source

{% if is_incremental() %}
where id not in (select id from {{ this }}) -- I will only load teams that are not in already
{% endif %}