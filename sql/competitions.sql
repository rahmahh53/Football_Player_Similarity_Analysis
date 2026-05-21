create database if not exists ml_data;

use ml_data;

drop table if exists competitions;

create table competitions(
    competition_id int,
    season_id int,
    country_name varchar(255),
    competition_name varchar(255),
    competition_youth boolean,
    competition_gender varchar(255),
    competition_international boolean,
    season_name varchar(255),
    match_updated datetime,
    match_updated_360 datetime,
    match_available_360 datetime,
    match_available datetime
);

load data local infile '/home/rah_mahh53/mlops/data/raw/competitions.csv' into table competitions fields terminated by ',' enclosed by '"' lines terminated by '\n' ignore 1 rows;

