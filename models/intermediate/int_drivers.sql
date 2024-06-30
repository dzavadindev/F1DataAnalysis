with drivers as (
    select * from {{ ref('stg_drivers') }}
),
driver_teams as (
    select * from {{ ref('stg_drivers_teams') }}
),
ranked_teams as (
    select
        driver_name,
        team,
        year,
        race_nr,
        row_number() over (partition by driver_name order by year desc, race_nr desc) as recency
    from driver_teams
),
latest_teams as (
    select
        driver_name,
        team
    from ranked_teams
    where recency = 1
)

select 
    d.id,
    d.full_name,
    d.code,
    lt.team
from drivers d
left join latest_teams lt on d.full_name = lt.driver_name
