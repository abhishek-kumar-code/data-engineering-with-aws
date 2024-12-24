from datetime import datetime, timedelta
import pendulum
import os
from airflow.decorators import dag
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.postgres_operator import PostgresOperator
from final_project_operators.stage_redshift import StageToRedshiftOperator
from final_project_operators.load_fact import LoadFactOperator
from final_project_operators.load_dimension import LoadDimensionOperator
from final_project_operators.data_quality import DataQualityOperator

from udacity.common.final_project_sql_statements import SqlQueries

default_args = {
    'owner': 'abhishek kumar',
    'start_date': pendulum.now(),
    'retries': 3,  # Retry the task up to 1 time if it fails
    'retry_delay': timedelta(minutes=5),  # Wait for 5 minutes before retrying
    'catchup': False
}

## Project Rubric: Dag configuration
# @dag decorates the final_project to denote it's the main function
# Setting cron expression to run the job at the start of every hour
@dag(
    default_args=default_args,
    description='Load and transform data in Redshift with Airflow',
    schedule_interval='0 * * * *'
)
def final_project():

    start_operator = DummyOperator(task_id='Begin_execution')

    ## Project Rubric: Staging the data

    # Post-events after 'final_project_create_table' DAG run is successfully completed

    # Stage 1: Load data to staging_events table
    # Using StageToRedshiftOperator Custom Operator to define the atomic steps of final_project DAG
     
    stage_events_to_redshift = StageToRedshiftOperator(
        task_id='Stage_events',
        table='staging_events',
        redshift_conn_id='redshift',
        aws_credentials_id='aws_credentials',
        s3_bucket='akumar-dend',
        s3_key='log-data',
        log_json_file='log_json_path.json'
    )

    # Stage 2: Load data to staging_songs table
    # Using StageToRedshiftOperator Custom Operator to define the atomic steps of final_project DAG

    stage_songs_to_redshift = StageToRedshiftOperator(
        task_id='Stage_songs',
        table='staging_songs',
        redshift_conn_id='redshift',
        aws_credentials_id='aws_credentials',
        s3_bucket='akumar-dend',
        s3_key='song-data/A/A/'
    )

    ## Project Rubric: Loading facts and dimensions 

    # Stage 3: Load data to songsplays fact table
    # Using LoadFactOperator Custom Operator to define the atomic steps of final_project DAG

    load_songplays_table = LoadFactOperator(
        task_id='Load_songplays_fact_table',
        redshift_conn_id='redshift',
        table='songplays',
        sql_query=SqlQueries.songplay_table_insert
    )

    # Stage 4: Load data to users dimension table
    # Using LoadDimensionOperator Custom Operator to define the atomic steps of final_project DAG

    load_user_dimension_table = LoadDimensionOperator(
        task_id='Load_user_dim_table',
        redshift_conn_id='redshift',
        table='users',
        sql_query=SqlQueries.user_table_insert,
        mode='truncate-insert'
    )

    # Stage 5: Load data to songs dimension table
    # Using LoadDimensionOperator Custom Operator to define the atomic steps of final_project DAG

    load_song_dimension_table = LoadDimensionOperator(
        task_id='Load_song_dim_table',
        redshift_conn_id='redshift',
        table='songs',
        sql_query=SqlQueries.song_table_insert,
        mode='truncate-insert'
    )

    # Stage 6: Load data to artists dimension table
    # Using LoadDimensionOperator Custom Operator to define the atomic steps of final_project DAG

    load_artist_dimension_table = LoadDimensionOperator(
        task_id='Load_artist_dim_table',
        redshift_conn_id='redshift',
        table='artists',
        sql_query=SqlQueries.artist_table_insert,
        mode='truncate-insert'
    )

    # Stage 7: Load data to time dimension table
    # Using LoadDimensionOperator Custom Operator to define the atomic steps of final_project DAG

    load_time_dimension_table = LoadDimensionOperator(
        task_id='Load_time_dim_table',
        redshift_conn_id='redshift',
        table='time',
        sql_query=SqlQueries.time_table_insert,
        mode='truncate-insert'
    )

    ## Project Rubric: Data Quality Checks

    # Stage 8: Data Quality Unit Tests
    # Using DataQualityOperator Custom Operator to define the atomic steps of final_project DAG

    data_quality_test = DataQualityOperator(
        task_id='Data_quality_test',
        redshift_conn_id='redshift',
        tables=['songplays', 'users', 'songs', 'artists', 'time']
    )

    end_operator = DummyOperator(task_id='Stop_execution')
    
    # Setting tasks dependencies

    # 1. Begin execution
    start_operator >> stage_events_to_redshift  # Start execution and stage data to Redshift
    start_operator >> stage_songs_to_redshift

    # 2. Load data into the Fact table (songplays)
    stage_events_to_redshift >> load_songplays_table  # Load data from events to the songplays table
    stage_songs_to_redshift >> load_songplays_table

    # 3. Load data into the Dimension tables
    load_songplays_table >> load_user_dimension_table  # Load data into the users dimension table
    load_songplays_table >> load_song_dimension_table  # Load data into the songs dimension table
    load_songplays_table >> load_artist_dimension_table  # Load data into the artists dimension table
    load_songplays_table >> load_time_dimension_table  # Load data into the time dimension table

    # 4. Run Data Quality Test after loading the dimension tables
    load_user_dimension_table >> data_quality_test  # Run the data quality test after all dimension tables are loaded
    load_song_dimension_table >> data_quality_test 
    load_artist_dimension_table >> data_quality_test 
    load_time_dimension_table >> data_quality_test 

    # 5. End execution
    data_quality_test >> end_operator  # End execution after the data quality test 
   
final_project_dag = final_project()