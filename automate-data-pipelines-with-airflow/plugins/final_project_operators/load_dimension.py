from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

# Custom Airflow Operator to move ingest data from AWS Redshift tables to custom dimension tables

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'

    @apply_defaults
    # Define your operators params (with defaults) here
    def __init__(self,
                 redshift_conn_id="",
                 sql_query="",
                 table="",
                 mode="append",
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        # Map params here
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.sql_query = sql_query
        self.mode = mode

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        self.log.info("Loading data from Redshift tables to dimension table")
        if self.mode == "truncate-insert":
            self.log.info("Truncating dimension tables before ingestion process")
        redshift.run("TRUNCATE TABLE {}".format(self.table))
        self.log.info("Ingesting data into dimension tables")
        redshift.run("INSERT INTO {} {}".format(self.table, self.sql_query))