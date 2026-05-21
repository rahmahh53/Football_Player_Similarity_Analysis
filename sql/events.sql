create database if not exists ml_data;

use ml_data;

create table events(
    id varchar(255),
    match_id int,
    type_name varchar(255),
    event_index int,
    possession int,
    possession_team varchar(255),
    location varchar(255),
    player varchar(255),
    shot text,
    carry text,
    duration float,
    minute int,
    second int
);


