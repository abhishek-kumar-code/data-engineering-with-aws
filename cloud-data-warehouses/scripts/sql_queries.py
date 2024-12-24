import configparser

# CONFIGURATION: Reads the configuration file ('dwh.cfg') that stores credentials and settings.
config = configparser.ConfigParser()
config.read('dwh.cfg')

# SQL QUERY SETUP: 
# The SQL queries will be defined here and used for creating, dropping, and loading data into the tables.

# DROP TABLES: These queries will drop any existing tables to ensure a clean slate for creating the staging and final tables.

## Staging Tables

# Drops the staging_events table if it exists
staging_events_table_drop = "DROP table IF EXISTS staging_events"
# Drops the staging_songs table if it exists
staging_songs_table_drop = "DROP table IF EXISTS staging_songs"  

## Fact Table

# Drops the songplays table if it exists
songplay_table_drop = "DROP table IF EXISTS songplays"  

## Dimension Table

# Drops the users table if it exists
user_table_drop = "DROP table IF EXISTS users" 
# Drops the songs table if it exists
song_table_drop = "DROP table IF EXISTS songs"  
# Drops the artists table if it exists
artist_table_drop = "DROP table IF EXISTS artists"  
# Drops the time table if it exists
time_table_drop = "DROP table IF EXISTS time"  

# CREATE TABLES: SQL queries to create the necessary tables in Redshift.
# These tables will store the raw and transformed data.

staging_events_table_create = ("""
    CREATE TABLE IF NOT EXISTS staging_events (
        artist              VARCHAR,
        auth                VARCHAR,
        firstName           VARCHAR,
        gender              CHAR(1),
        itemInSession       INT,
        lastName            VARCHAR,
        length              FLOAT,
        level               VARCHAR,
        location            TEXT,
        method              VARCHAR,
        page                VARCHAR,
        registration        FLOAT,
        sessionId           INT,
        song                VARCHAR,
        status              INT,
        ts                  BIGINT,
        userAgent           TEXT,
        userId              VARCHAR);
""")

staging_songs_table_create = ("""
CREATE TABLE IF NOT EXISTS staging_songs (
	 artist_id           VARCHAR,
        artist_latitude     FLOAT,
        artist_location     TEXT,
        artist_longitude    FLOAT,
        artist_name         VARCHAR,
        duration            FLOAT,
        num_songs           INT,
        song_id             VARCHAR,
        title               VARCHAR,
        year                INT);
""")

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays
    (songplay_id bigint IDENTITY(0,1) PRIMARY KEY,  
     start_time timestamp NOT NULL,  
     user_id varchar(256) NOT NULL, 
     level varchar(256),  
     song_id varchar(256), 
     artist_id varchar(256) NOT NULL,  
     session_id int, 
     location varchar(256),  
     user_agent varchar(256)  
);
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users 
(
    user_id varchar(256) PRIMARY KEY,  
    first_name varchar(256),  
    last_name varchar(256),  
    gender char, 
    level varchar(256)  
);
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs 
(
    song_id varchar(256) PRIMARY KEY,  
    title varchar(256),  
    artist_id varchar(256),  
    year int,  
    duration float  
);
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists 
(
    artist_id varchar(256) PRIMARY KEY, 
    name varchar(256), 
    location varchar(256),  
    latitude float, 
    longitude float 
);
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time 
(
    start_time timestamp PRIMARY KEY,  
    hour int, 
    day int,  
    week int,  
    month int, 
    year int,  
    weekday int 
);
""")

# STAGING TABLES: These queries load data into the staging tables from S3.

staging_events_copy = ("""COPY staging_events FROM {}
                            iam_role {}
                            format as json {}
                            region 'us-west-2';
""").format(config['S3']['LOG_DATA'], config['IAM_ROLE']['ARN'], config['S3']['LOG_JSONPATH'])

staging_songs_copy = ("""COPY staging_songs FROM {}
                        iam_role {}
                        format as json 'auto'
                        region 'us-west-2';
""").format(config['S3']['SONG_DATA'], config['IAM_ROLE']['ARN'])

# FINAL TABLES: These queries insert data into the final tables from the staging tables.

songplay_table_insert = ("""
INSERT INTO songplays (start_time, 
    user_id, level, song_id, artist_id, session_id, location, user_agent)
    SELECT DISTINCT(DATEADD(s, e.ts/1000, '19700101')) AS start_time,  
    e.userId AS user_id,
    e.level,
    s.song_id,
    s.artist_id,
    e.sessionId AS session_id,
    e.location,
    e.userAgent AS user_agent
    FROM staging_events  e
    JOIN staging_songs s ON (e.song = s.title
    AND e.length = s.duration
    AND e.artist = s.artist_name)
    WHERE e.page='NextSong'  
""")

user_table_insert = ("""
INSERT INTO users (user_id, first_name, last_name, gender, level)
    SELECT DISTINCT s.userId AS user_id,
    s.firstName AS first_name,
    s.lastName AS last_name,
    s.gender,
    s.level
    FROM staging_events s
    WHERE s.page NOT IN('Login', 'Home', 'About', 'Help') 
""")

song_table_insert = ("""
INSERT INTO songs (song_id, title, artist_id, year, duration)
    SELECT DISTINCT song_id,
    title,
    artist_id,
    year,
    duration
    FROM staging_songs
""")

artist_table_insert = ("""
INSERT INTO artists (artist_id, name, location, latitude, longitude)
    SELECT DISTINCT artist_id,
    artist_name AS name,
    artist_location AS location,
    artist_latitude AS latitude,
    artist_longitude AS longitude
    FROM staging_songs
""")

time_table_insert = ("""
INSERT INTO time (start_time, hour, day, week, month, year, weekday)
    SELECT DISTINCT(DATEADD(s, ts/1000, '19700101')) AS start_time,  
    EXTRACT(hour from start_time) AS hour,
    EXTRACT(day from start_time) AS day,
    EXTRACT(week from start_time) AS week,
    EXTRACT(month from start_time) AS month,
    EXTRACT(year from start_time) AS year,
    EXTRACT(weekday from start_time) AS weekday
    FROM staging_events
""")

# QUERY LISTS: List of all queries for easy iteration and execution.

drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, 
                      songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]

create_table_queries = [staging_events_table_create, staging_songs_table_create, 
                        songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]

copy_table_queries = [staging_events_copy, staging_songs_copy]

insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
