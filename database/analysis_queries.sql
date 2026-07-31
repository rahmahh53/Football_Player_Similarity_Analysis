-- =========================================================
-- passing analysis
-- =========================================================

-- players with the highest pass-completion percentage
-- minimum 1,000 attempted passes

select p.player_name, count(*) as total_passes,
    sum(case when pa.outcome_id is null then 1 else 0 end) as completed_passes,
    round(100.0 * sum(case when pa.outcome_id is null then 1 else 0 end)/count(*), 2) as completion_percentage
    from events as e join players as p on e.player_id = p.player_id
    join passes as pa on e.event_id = pa.event_id
    group by p.player_id, p.player_name
    having count(*) >= 1000 order by completion_percentage desc, completed_passes desc limit 20;


-- players with the most attempted passes

select p.player_id, p.player_name, count(*) as total_passes from events as e
    join passes as pa on e.event_id = pa.event_id join players as p on e.player_id = p.player_id
    group by p.player_id, p.player_name order by total_passes desc limit 20;


-- outfield players with the highest average pass length
-- goalkeeper position_id = 1 excluded

select p.player_id, p.player_name, count(*) as total_passes, round(avg(pa.length), 2) as average_pass_length
    from events as e join passes as pa on e.event_id = pa.event_id join players as p on e.player_id = p.player_id
    where e.position_id <> 1 group by p.player_id, p.player_name having count(*) >= 100 order by average_pass_length desc limit 20;

-- =========================================================
-- progressive passing analysis
-- =========================================================

-- successful passes advancing the ball by at least 10 units
-- goalkeeper events excluded
-- minimum 500 attempted passes

select p.player_id, p.player_name, count(*) as total_passes,
sum(case when pa.outcome_id is null and pa.end_location_x - e.location_x >= 10 then 1 else 0 end) as progressive_passes,
round(100 * sum(case when pa.outcome_id is null and pa.end_location_x - e.location_x >= 10 then 1 else 0 end)/count(*), 2) as progressive_pass_percentage
from events as e join players as p on e.player_id = p.player_id join passes as pa on e.event_id = pa.event_id
where e.position_id <> 1 group by p.player_id, p.player_name having count(*) >= 500 order by progressive_pass_percentage desc;


-- Progressive passing volume (minimum 500 passes)

select  p.player_name, count(*) as total_passes,
sum(case when pa.outcome_id is null and pa.end_location_x - e.location_x >= 10 then 1 else 0 end) as progressive_passes,
round(100 * sum(case when pa.outcome_id is null and pa.end_location_x - e.location_x >= 10 then 1 else 0 end)/count(*), 2) as progressive_pass_percentage
from events as e join players as p on e.player_id = p.player_id join passes as pa on e.event_id = pa.event_id
where e.position_id <> 1 group by p.player_id, p.player_name having count(*) >= 500 order by progressive_passes desc;


-- =====================================================
-- shooting analysis
-- =====================================================

-- players with the highest shooting accuracy
select p.player_name, count(*) as total_shots,
sum(case when s.outcome_id in (97, 100, 116) then 1 else 0 end) as shots_on_target,
round(100.0 * sum(case when s.outcome_id in (97, 100, 116) then 1 else 0 end)/count(*), 2) as shooting_accuracy
from events as e join players as p on e.player_id = p.player_id join shots as s on e.event_id = s.event_id
group by p.player_id, p.player_name having count(*) >= 50 order by shooting_accuracy desc;

-- players with the highest goal conversion rate
select p.player_name, count(*) as total_shots,
sum(case when s.outcome_id = 97 then 1 else 0 end) as goals,
round(100.0 * sum(case when s.outcome_id = 97 then 1 else 0 end)/count(*), 2) as goal_conversion_rate
from events as e join players as p on e.player_id = p.player_id join shots as s on e.event_id = s.event_id
group by p.player_id, p.player_name having count(*) >= 50 order by goal_conversion_rate desc;


-- =====================================================
-- attacking metrics
-- =====================================================


select p.player_name, sum(case when pa.event_id is not null and pa.outcome_id is null then 1 else 0 end) as completed_passes,
sum(case when d.outcome_id = 8 then 1 else 0 end) as successful_dribbles, count(s.event_id) as shots,
(sum(case when pa.event_id is not null and pa.outcome_id is null then 1 else 0 end) + sum(case when d.outcome_id = 8 then 1 else 0 end) + count(s.event_id)) as total_attacking_actions
from events as e join players as p on e.player_id = p.player_id left join passes as pa on e.event_id = pa.event_id
left join dribbles as d on e.event_id = d.event_id left join shots as s on e.event_id = s.event_id
group by p.player_name, p.player_id order by total_attacking_actions desc;


--most successful dribbles

select p.player_name, count(*) as total_dribbles, sum(case when d.outcome_id = 8 then 1 else 0 end) as successful_dribbles,
rount(100.0 * sum(case when d.outcome_id = 8 then 1 else 0 end)/count(*), 2) as success_rate from events as e join players as p on
e.player_id = p.player_id join dribbles as d on e.event_id = d.event_id group by p.player_id, p.player_name
having count(*) >= 50 order by successful_dribbles desc;

--dribbles success rate

select p.player_name, count(*) as total_dribbles, sum(case when d.outcome_id = 8 then 1 else 0 end) as successful_dribbles,
round(100.0 * sum(case when d.outcome_id = 8 then 1 else 0 end)/count(*), 2) as success_rate from events as e join players as p on
e.player_id = p.player_id join dribbles as d on e.event_id = d.event_id group by p.player_id, p.player_name
having count(*) >= 50 order by success_rate desc;

--most shots taken

select p.player_name, count(*) as total_shots from events as e join players as p on e.player_id = p.player_id
join shots as s on e.event_id = s.event_id group by p.player_id, p.player_name order by total_shots desc;

--most passes per match

select p.player_name, count(*) as total_passes, count(distinct e.match_id) as total_matches, round(1.0 * count(*)/count(distinct e.match_id), 2) as passes_per_match from events as e 
join players as p on e.player_id = p.player_id join passes as pa on e.event_id = pa.event_id group by p.player_name, p.player_id 
having count(distinct e.match_id) >= 5 order by passes_per_match desc;

-- =========================================================
-- ball progression analysis
-- =========================================================

-- most progressive passes per match

select p.player_name, count(distinct e.match_id) as total_matches, sum(case when pa.outcome_id is null and pa.end_location_x - e.location_x >= 10 then 1 else 0 end) as progressive_passes,
round(1.0 * sum(case when pa.outcome_id is null and pa.end_location_x - e.location_x >= 10 then 1 else 0 end)/count(distinct e.match_id), 2) as progressive_passes_per_match from events as e 
join players as p on e.player_id = p.player_id join passes as pa on e.event_id = pa.event_id where e.position_id <> 1 group by p.player_id, p.player_name
having count(distinct e.match_id) >= 10 order by progressive_passes_per_match desc;

-- most progressive carries per match

select p.player_name, count(distinct e.match_id) as total_matches, count(*) as total_carries,
sum(case when c.end_location_x - e.location_x >= 10 then 1 else 0 end) as progressive_carries,
round(1.0 * sum(case when c.end_location_x - e.location_x >= 10 then 1 else 0 end)/count(distinct e.match_id), 2) as progressive_carries_per_match
from events as e join players as p on e.player_id = p.player_id join carries as c on e.event_id = c.event_id
where e.position_id <> 1 group by p.player_id, p.player_name having count(distinct e.match_id) >= 10
order by progressive_carries_per_match desc;

-- highest duel success rate

select p.player_name, count(*) as total_duels, sum(case when d.outcome_id in (4, 15, 16, 17) then 1 else 0 end) as successful_duels, 
round(100.0 * sum(case when d.outcome_id in (4, 15, 16, 17) then 1 else 0 end)/count(*), 2) as duel_success_rate from events as e 
join players as p on e.player_id = p.player_id join duels as d on e.event_id = d.event_id group by p.player_name, p.player_id having count(*) >= 50
order by duel_success_rate desc;

-- most duels 

select p.player_name, count(*) as total_duels, sum(case when d.outcome_id in (4, 15, 16, 17) then 1 else 0 end) as successful_duels, 
round(100.0 * sum(case when d.outcome_id in (4, 15, 16, 17) then 1 else 0 end)/count(*), 2) as duel_success_rate from events as e 
join players as p on e.player_id = p.player_id join duels as d on e.event_id = d.event_id group by p.player_name, p.player_id having count(*) >= 50
order by total_duels desc;

-- shots analysis

select p.player_name, count(*) as total_shots, round(sum(s.statsbomb_xg), 2) as total_xg, round(avg(s.statsbomb_xg), 3) as average_xg_per_shot, 
sum(case when s.outcome_id = 97 then 1 else 0 end) as goals, round(sum(case when s.outcome_id = 97 then 1 else 0 end) - sum(s.statsbomb_xg), 2) as goals_minus_xg
from events as e join players as p on e.player_id = p.player_id join shots as s on e.event_id = s.event_id group by p.player_id,
p.player_name having count(*) >= 50 order by goals_minus_xg desc;

