from datetime import datetime, timedelta
import pendulum
import os
from airflow.decorators import dag
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.postgres_operator import PostgresOperator
from udacity.common import final_project_create_tables

default_args = {
    'owner': 'abhishek kumar',
    'start_date': pendulum.now(),
    'retries': 3,  # Retry the task up to 1 time if it fails
    'retry_delay': timedelta(minutes=5),  # Wait for 5 minutes before retrying
    'catchup': False
}

# Project Rubric: Dag configuration
# @dag decorates the final_project_create_table to denote it's the main function
# Setting cron expression to run the job at the start of every hour
@dag(
    default_args=default_args,
    description='Pre-processing Stage: Creating empty tables in Redshift using DAG',
    schedule_interval='0 * * * *'
)
def final_project_create_table():

    start_operator = DummyOperator(task_id='Begin_execution')
    
    # Using PostgresOperator Operator to define the atomic steps of final_project_create_table DAG

    # Drop and Create TBL#1 staging_events

    drop_staging_events_table = PostgresOperator(
        task_id='drop_table_staging_events',
        postgres_conn_id='redshift',
        sql=final_project_create_tables.DROP_STAGING_EVENTS_TABLE_SQL
    )
    create_staging_events_table=PostgresOperator(
        task_id="create_table_staging_events",
        postgres_conn_id="redshift",
        sql=final_project_create_tables.CREATE_STAGING_EVENTS_TABLE_SQL
    )

    # Drop and Create TBL#2 staging_songs

    drop_staging_songs_table = PostgresOperator(
        task_id='drop_table_staging_songs',
        postgres_conn_id='redshift',
        sql=final_project_create_tables.DROP_STAGING_SONGS_TABLE_SQL
    )
    create_staging_songs_table=PostgresOperator(
        task_id="create_table_staging_songs",
        postgres_conn_id="redshift",
        sql=final_project_create_tables.CREATE_STAGING_SONGS_TABLE_SQL
    )

    # Drop and Create TBL#3 songplays

    drop_songplays_table = PostgresOperator(
        task_id='drop_table_songsplays',
        postgres_conn_id='redshift',
        sql=final_project_create_tables.DROP_SONGPLAYS_TABLE_SQL
    )
    create_songplays_table=PostgresOperator(
        task_id="create_table_songplays",
        postgres_conn_id="redshift",
        sql=final_project_create_tables.CREATE_SONGPLAYS_TABLE_SQL
    )

    # Drop and Create TBL#4 users

    drop_users_table = PostgresOperator(
        task_id='drop_table_users',
        postgres_conn_id='redshift',
        sql=final_project_create_tables.DROP_USERS_TABLE_SQL
    )
    create_users_table=PostgresOperator(
        task_id="create_table_users",
        postgres_conn_id="redshift",
        sql=final_project_create_tables.CREATE_USERS_TABLE_SQL
    )

    # Drop and Create TBL#5 songs

    drop_songs_table = PostgresOperator(
        task_id='drop_table_songs',
        postgres_conn_id='redshift',
        sql=final_project_create_tables.DROP_SONGS_TABLE_SQL
    )
    create_songs_table=PostgresOperator(
        task_id="create_table_songs",
        postgres_conn_id="redshift",
        sql=final_project_create_tables.CREATE_SONGS_TABLE_SQL
    )

    # Drop and Create TBL#6 artists

    drop_artists_table = PostgresOperator(
        task_id='drop_table_artists',
        postgres_conn_id='redshift',
        sql=final_project_create_tables.DROP_ARTISTS_TABLE_SQL
    )
    create_artists_table=PostgresOperator(
        task_id="create_table_artists",
        postgres_conn_id="redshift",
        sql=final_project_create_tables.CREATE_ARTISTS_TABLE_SQL
    )

    # Drop and Create TBL#7 time

    drop_time_table = PostgresOperator(
        task_id='drop_table_time',
        postgres_conn_id='redshift',
        sql=final_project_create_tables.DROP_TIME_TABLE_SQL
    )
    create_time_table=PostgresOperator(
        task_id="create_table_time",
        postgres_conn_id="redshift",
        sql=final_project_create_tables.CREATE_TIME_TABLE_SQL
    )

    end_operator = DummyOperator(task_id='Stop_execution')

    # Setting tasks dependencies

    # Start Execution
    start_operator >> drop_staging_events_table >> create_staging_events_table
    start_operator >> drop_staging_songs_table >> create_staging_songs_table

    # Staging tables to Fact table (songplays)
    create_staging_events_table >> drop_songplays_table >> create_songplays_table
    create_staging_songs_table >> drop_songplays_table >> create_songplays_table

    # Fact table (songplays) and Staging tables to Dimension tables (users, songs, artists, time)
    create_songplays_table >> drop_users_table >> create_users_table
    create_songplays_table >> drop_songs_table >> create_songs_table
    create_songplays_table >> drop_artists_table >> create_artists_table
    create_songplays_table >> drop_time_table >> create_time_table

    # End Execution
    create_time_table >> end_operator

final_project_create_table_dag = final_project_create_table()