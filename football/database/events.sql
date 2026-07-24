create database if not exists ml_data;

use ml_data;

create table events(
    id varchar(255),
    match_id int,
    type_name varchar(255),
    event_index int,
    minute int,
    second int,
    timestamp varchar(50),
    period int,
    possession int,
    possession_team_name varchar(255),
    team_name varchar(255),
    location_x float,
    location_y float,
    player_name varchar(255),
    shot_outcome text,
    pass_outcome text,
    carry_end_x float,
    carry_end_y float,
    duration float
);

load data local infile '/home/rah_mahh53/mlops/data/processed_data/events_flat.csv' into table events fields terminated by ',' enclosed by '"' lines terminated by '\n' ignore 1 rows;
