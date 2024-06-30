with source as (
    select * from {{ source('raw_data', 'raw_drivers') }}
)

select 
    id,
    cast(number as int) as drivers_number,
    code,
    concat(first_name, ' ', last_name) as full_name,
    strptime(date_of_birth, '%Y-%m-%d')::DATE as date_of_birth,
    country
from source

{% if is_incremental() %}
where id not in (select id from {{ this }}) -- I will only load records after the current latest (should be like 2023?) 
{% endif %}