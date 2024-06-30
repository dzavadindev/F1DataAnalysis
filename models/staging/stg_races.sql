with source as (
      select * from {{ source('raw_data', 'raw_races') }}
)

select 
    race,
    strptime(date, '%Y-%m-%d')::DATE as date
from source

{% if is_incremental() %}
where date > (select max(date) from {{ this }}) -- I will only load records after the current latest (should be like 2023?) 
{% endif %}