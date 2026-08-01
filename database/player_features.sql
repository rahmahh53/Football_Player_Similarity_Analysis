-- =========================================================
-- player modeling feature dataset
-- one row per player
-- =========================================================

with pass_features as (select e.player_id, count(*) as total_passes, sum(case when pa.outcome_id is null then 1 else 0 end) as completed_passes,
sum(case when pa.outcome_id is null and pa.end_location_x - e.location_x >= 10 then 1 else 0 end) as progressive_passes from events as e join passes as pa
on e.event_id = pa.event_id group by e.player_id),
    shot_features as (select e.player_id, count(*) as total_shots, sum(case when s.outcome_id = 97 then 1 else 0 end) as goals, sum(s.statsbomb_xg) as total_xg
    from events as e join shots as s on e.event_id = s.event_id group by e.player_id),
    dribble_features as (select e.player_id, count(*) as total_dribbles, sum(case when d.outcome_id = 8 then 1 else 0 end) as successful_dribbles
    from events as e join dribbles as d on e.event_id = d.event_id group by e.player_id),
    carry_features as (select e.player_id, count(*) as total_carries, sum(case when c.end_location_x - e.location_x >= 10 then 1 else 0 end) as progressive_carries
    from events as e join carries as c on e.event_id = c.event_id group by e.player_id),
    appearance_features as (select player_id, count(distinct match_id) as matches_played
    from events where player_id is not null group by player_id)
select p.player_id, p.player_name, coalesce(pf.total_passes, 0) as total_passes, coalesce(pf.completed_passes, 0) as completed_passes, coalesce(pf.progressive_passes, 0) as progressive_passes, round(100.0 * coalesce(pf.completed_passes, 0)/nullif(pf.total_passes, 0), 2) as pass_completion_rate,
round(1.0 * coalesce(pf.total_passes, 0)/nullif(af.matches_played, 0), 2) as passes_per_match, round(1.0 * coalesce(pf.progressive_passes, 0)/nullif(af.matches_played, 0), 2) as progressive_passes_per_match,
round(100.0 * coalesce(pf.progressive_passes, 0)/ nullif(pf.total_passes, 0), 2) as progressive_pass_rate,
coalesce(sf.total_shots, 0) as total_shots, coalesce(sf.goals, 0) as goals, round(1.0 * coalesce(sf.total_xg, 0), 2) as total_xg, round(1.0 * coalesce(sf.total_shots, 0)/nullif(af.matches_played, 0), 2) as shots_per_match, 
round(1.0 * coalesce(sf.goals, 0)/nullif(af.matches_played, 0), 2) as goals_per_match, round(1.0 * coalesce(sf.total_xg, 0)/nullif(af.matches_played, 0), 2) as xg_per_match,
round(1.0 * coalesce(sf.total_xg, 0)/nullif(sf.total_shots, 0), 2) as average_xg_per_shot, round(coalesce(sf.goals, 0) - coalesce(sf.total_xg, 0), 2) as goals_minus_xg,
coalesce(df.total_dribbles, 0) as total_dribbles, coalesce(df.successful_dribbles, 0) as successful_dribbles, round(1.0 * coalesce(df.total_dribbles, 0)/nullif(af.matches_played, 0), 2) as dribbles_per_match, coalesce(round(100.0 * coalesce(df.successful_dribbles, 0)/nullif(df.total_dribbles, 0), 2), 0) as dribble_success_rate,
coalesce(cf.total_carries, 0) as total_carries, coalesce(cf.progressive_carries, 0) as progressive_carries, round(1.0 * coalesce(cf.total_carries, 0)/nullif(af.matches_played, 0), 2) as carries_per_match, round(1.0 * coalesce(cf.progressive_carries, 0)/nullif(af.matches_played, 0), 2) as progressive_carries_per_match,
coalesce(af.matches_played, 0) as matches_played from players as p left join pass_features as pf on p.player_id = pf.player_id
left join shot_features as sf on p.player_id = sf.player_id left join dribble_features as df on p.player_id = df.player_id
left join carry_features as cf on p.player_id = cf.player_id left join appearance_features as af on p.player_id = af.player_id where coalesce(af.matches_played, 0) >= 5;
