with races as (
    select
        year,
        races_amount,
        first_place_points,
        races_amount * first_place_points as max_available_points
    from {{ ref('dim_races') }}
),
teams as (
    select
        id as team_id,
        name as team_name
    from {{ ref('dim_teams') }}
),
points as (
    select
        year,
        team,
        count(distinct race_name) as races_finished,
        sum(points) as total_points,
        avg(points) as average_points
    from {{ ref('fct_points') }}
    group by year, team
),
combined_calc as (
    select
        p.year,
        p.team,
        p.total_points + (r.races_amount - p.races_finished) * p.average_points as predicted_points,
        p.total_points + (r.races_amount - p.races_finished) * r.first_place_points as potential_points,
        r.max_available_points
    from points p
    join races r on p.year = r.year
    join teams t on p.team = t.team_name
),
normalization as (
    select
        year,
        max(predicted_points) as maximum_predicted_of_set,
        min(predicted_points) as minimum_predicted_of_set
    from combined_calc
    group by year
),
normalized_predictions as (
    select
        cc.year,
        cc.team,
        cc.predicted_points,
        cc.potential_points,
        ((cc.predicted_points - n.minimum_predicted_of_set) / nullif(n.maximum_predicted_of_set - n.minimum_predicted_of_set, 0)) * cc.max_available_points as normalized_predicted_points
    from combined_calc cc
    join normalization n on cc.year = n.year
),
ranked_teams as (
    select
        year,
        team,
        predicted_points,
        potential_points,
        normalized_predicted_points
    from normalized_predictions
)

select
    year,
    team,
    max(potential_points) as potential_points,
    floor(max(normalized_predicted_points)) as predicted_points,
from ranked_teams 
group by year, team
order by predicted_points desc
