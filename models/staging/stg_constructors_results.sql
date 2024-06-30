with source as (
    select * from {{ source('raw_data', 'raw_constructors_results') }}
)

select
    cast(year as INT) as year,
    cast(round as INT) as round,
    name as race_name,
    strptime(date, '%Y-%m-%d')::DATE as date,
    team,
    cast(points as int) as points
from source

{% if is_incremental() %}
where date > (select max(date) from {{ this }}) -- I will only load records after the current latest (should be like 2023?) 
{% endif %}