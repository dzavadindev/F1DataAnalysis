with source as (
    select * from {{ source('raw_data', 'raw_drivers_teams') }}
)

select
    driver as driver_name,
    name as team,
    cast(year as INT) as year,
    cast(race_nr as INT) as race_nr
from source

{% if is_incremental() %}
where year > (select max(year) from {{ this }}) -- I will only load records after the current latest (should be like 2023?) 
{% endif %}