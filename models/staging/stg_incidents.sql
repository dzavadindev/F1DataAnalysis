with source as (
      select * from {{ source('raw_data', 'raw_incidents') }}
)

select 
    strptime(date, '%Y-%m-%d')::DATE as date,
    strptime(time, '%H:%M:%S')::TIMESTAMP as time,
    cast(driver_one_num as INT) as driver_one_num,
    cast(driver_two_num as INT) as driver_two_num,
    driver_one_code,
    driver_two_code,
    race
FROM source

{% if is_incremental() %}
where date > (select max(date) from {{ this }}) -- I will only load records after the current latest (should be like 2023?) 
{% endif %}