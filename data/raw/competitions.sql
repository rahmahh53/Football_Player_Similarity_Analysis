create database if not exists ml_data;

use ml_data;

drop table if exists competitions;

create table competitions(
    competition_id varchar(255),
    season_id varchar(255),
    country_name varchar(255),
    competition_name varchar(255),
    competition_youth varchar(255),
    competition_international varchar(255),
    season_name varchar(255),
    match_updated varchar(255),
    match_updated_360 varchar(255),
    match_available_360 varchar(255),
    match_available  varchar(255)
);

load data local infile 'competitions.csv' into table competitions fields terminated by ',' enclosed by '"' lines terminated by '\n' ignore 1 rows;

