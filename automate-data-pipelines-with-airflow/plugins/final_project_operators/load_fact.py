from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

# Custom Airflow Operator to move data from staging_events to AWS Redshift songplay_table tables

class LoadFactOperator(BaseOperator):

    ui_color = '#F98866'

    @apply_defaults
    # Define your operators params (with defaults) here
    def __init__(self,
                 redshift_conn_id="",
                 table="",
                 sql_query="",
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        # Map params here
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.sql_query = sql_query

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        self.log.info("Loading data from staging_events table to songplays fact table")
        redshift.run("INSERT INTO {} {}".format(self.table, self.sql_query))
