with drivers as (
    select * from {{ ref('dim_drivers') }}
),
teams as (
    select * from {{ ref("dim_teams") }}
),
incidents as (
    select 
        *, 
        YEAR(date) as year
    from 
        {{ ref('fct_incidents') }}
),
driver_one_counts as (
    select
        driver_one_code as driver_code,
        year,
        count(*) as incident_count
    from
        incidents
    group by
        driver_one_code, year
),
driver_two_counts as (
    select
        driver_two_code as driver_code,
        year,
        count(*) as incident_count
    from
        incidents
    group by
        driver_two_code, year
),
total_incident_count as (
    select 
        driver_code,
        year,
        sum(incident_count) as total_incidents
    from (
        select
            driver_code,
            year,
            incident_count
        from driver_one_counts
        union all
        select 
            driver_code,
            year,
            incident_count
        from driver_two_counts
    ) combined
    group by driver_code, year
) 

select DISTINCT
    d.full_name,
    d.team,
    t.year,
    coalesce(t.total_incidents, 0) as total_incidents
from 
    drivers d
left join total_incident_count t on d.code = t.driver_code
order by t.year, total_incidents desc
