import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality
from awsglue import DynamicFrame

def sparkSqlQuery(glueContext, query, mapping, transformation_ctx) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(query)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Default ruleset used by all target nodes with data quality enabled
DEFAULT_DATA_QUALITY_RULESET = """
    Rules = [
        ColumnCount > 0
    ]
"""

# Script generated for node S3: customer_trusted
S3customer_trusted_node1733344539223 = glueContext.create_dynamic_frame.from_catalog(database="stedi-hb", table_name="customer_trusted", transformation_ctx="S3customer_trusted_node1733344539223")

# Script generated for node S3: accelerometer_landing
S3accelerometer_landing_node1733344531594 = glueContext.create_dynamic_frame.from_catalog(database="stedi-hb", table_name="accelerometer_landing", transformation_ctx="S3accelerometer_landing_node1733344531594")

# Script generated for node Customer Privacy Filter
CustomerPrivacyFilter_node1733344588791 = Join.apply(frame1=S3customer_trusted_node1733344539223, frame2=S3accelerometer_landing_node1733344531594, keys1=["email"], keys2=["user"], transformation_ctx="CustomerPrivacyFilter_node1733344588791")

# Script generated for node SQL Query
SqlQuery2790 = '''
select user, timestamp, x, y, z from myDataSource;
'''
SQLQuery_node1733347944651 = sparkSqlQuery(glueContext, query = SqlQuery2790, mapping = {"myDataSource":CustomerPrivacyFilter_node1733344588791}, transformation_ctx = "SQLQuery_node1733347944651")

# Script generated for node S3: accelerometer_trusted
EvaluateDataQuality().process_rows(frame=SQLQuery_node1733347944651, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1733344472649", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
S3accelerometer_trusted_node1733344718199 = glueContext.getSink(path="s3://stedi-hb-lake-house/accelerometer/trusted/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="S3accelerometer_trusted_node1733344718199")
S3accelerometer_trusted_node1733344718199.setCatalogInfo(catalogDatabase="stedi-hb",catalogTableName="accelerometer_trusted")
S3accelerometer_trusted_node1733344718199.setFormat("json")
S3accelerometer_trusted_node1733344718199.writeFrame(SQLQuery_node1733347944651)
job.commit()