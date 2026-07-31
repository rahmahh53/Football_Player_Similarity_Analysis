-- row counts

select count(*) as competitions_count from competitions;
select count(*) as seasons_count from seasons;
select count(*) as matches_count from matches;
select count(*) as players_count from players;
select count(*) as events_count from events;
select count(*) as passes_count from passes;
select count(*) as shots_count from shots;
select count(*) as carries_count from carries;
select count(*) as dribbles_count from dribbles;
select count(*) as duels_count from duels;


-- orphaned pass records

select count(*) as orphaned_passes from passes as pa left join events as e on pa.event_id = e.event_id where e.event_id is null;

-- events without matching matches

select count(*) as events_without_matches from events as e left join matches as m on e.match_id = m.match_id where m.match_id is null;

-- events with invalid players

select count(*) as invalid_event_players from events as e left join players as p on e.player_id = p.player_id where e.player_id is not null and p.player_id is null;
