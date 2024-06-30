with source as (
      select * from {{ source('raw_data', 'raw_races_carried_out') }}
)

select 
    cast(year as INT) as year,
    cast (number_of_races as int) races_amount,
    cast (first_place_points as int) first_place_points
from source

{% if is_incremental() %}
where year > (select max(year) from {{ this }}) -- I will only load records after the current latest 
{% endif %}