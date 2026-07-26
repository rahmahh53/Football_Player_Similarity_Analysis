-- table creation order
--
-- competitions
-- seasons
-- countries
-- teams
-- players
-- matches
-- lineups
-- events
-- passes
-- shots
-- carries
-- dribbles
-- duels


create table if not exists competitions (
    competition_id int primary key,
    competition_name varchar(255),
    country_name varchar(255)
);

create table if not exists seasons (
    season_id int primary key,
    season_name varchar(255),
    competition_id int,

    foreign key (competition_id) references competitions(competition_id)
);

create table if not exists countries(
    country_id int primary key,
    country_name varchar(255) not null
);

create table if not exists teams(
    team_id int primary key,
    team_name varchar(255) not null
);

create table if not exists players (
    player_id int primary key,
    player_name varchar(255) not null,
    country_id int,

    foreign key (country_id) references countries(country_id)
);

create table if not exists matches (
    match_id int primary key,
    match_date date,
    match_week int,
    home_score int,
    away_score int,
    home_team_id int,
    away_team_id int,
    competition_id int,
    season_id int,
    competition_stage int,

    foreign key (competition_id) references competitions(competition_id),
    foreign key (season_id) references seasons(season_id),
    foreign key (home_team_id) references teams(team_id),
    foreign key (away_team_id) references teams(team_id)
);

create table if not exists lineups (
    match_id int,
    team_id int,
    player_id int,
    jersey_number int,

    primary key (match_id, player_id),

    foreign key (match_id) references matches(match_id),
    foreign key (team_id) references teams(team_id),
    foreign key (player_id) references players(player_id)
);

create table if not exists events(
    event_id char(36) primary key,
    match_id int not null,
    event_index int not null,
    period int not null,
    timestamp varchar(20) not null,
    minute int not null,
    second int not null,
    possession int not null,
    possession_team_id int not null,
    team_id int not null,
    position_id int,
    duration double,
    under_pressure boolean,
    event_type varchar(100) not null,
    player_id int,
    location_x double,
    location_y double,

    foreign key (match_id) references matches(match_id),
    foreign key (possession_team_id) references teams(team_id),
    foreign key (team_id) references teams(team_id),
    foreign key (player_id) references players(player_id)
);

create table if not exists passes(
    event_id char(36) primary key,
    recipient_id int,
    length double,
    outcome_id int,
    end_location_x double,
    end_location_y double,

    foreign key (event_id) references events(event_id),
    foreign key (recipient_id) references players(player_id)
);


create table if not exists shots(
    event_id char(36) primary key,
    statsbomb_xg double not null,
    key_pass_id char(36),
    outcome_id int,
    first_time boolean,
    technique_id int,
    body_part_id int,
    shot_type_id int,
    end_location_x double,
    end_location_y double,
    end_location_z double,

    foreign key (event_id) references events(event_id)
);


create table if not exists carries(
    event_id char(36) primary key,
    end_location_x double,
    end_location_y double,

    foreign key (event_id) references events(event_id)
);


create table if not exists dribbles(
    event_id char(36) primary key,
    nutmeg boolean,
    outcome_id int,

    foreign key (event_id) references events(event_id)
);


create table if not exists duels(
    event_id char(36) primary key,
    duel_type_id int,

    foreign key (event_id) references events(event_id)
);
