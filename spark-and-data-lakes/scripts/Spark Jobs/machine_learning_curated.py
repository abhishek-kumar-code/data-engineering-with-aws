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

# Script generated for node S3: step_trainer_landing
S3step_trainer_landing_node1733371480855 = glueContext.create_dynamic_frame.from_catalog(database="stedi-hb", table_name="step_trainer_landing", transformation_ctx="S3step_trainer_landing_node1733371480855")

# Script generated for node S3: customer_trusted
S3customer_trusted_node1733371437293 = glueContext.create_dynamic_frame.from_catalog(database="stedi-hb", table_name="customer_trusted", transformation_ctx="S3customer_trusted_node1733371437293")

# Script generated for node S3: accelerometer_trusted
S3accelerometer_trusted_node1733372684665 = glueContext.create_dynamic_frame.from_catalog(database="stedi-hb", table_name="accelerometer_trusted", transformation_ctx="S3accelerometer_trusted_node1733372684665")

# Script generated for node SQL Query
SqlQuery2962 = '''
SELECT 
stl.serialnumber, stl.sensorreadingtime, stl.distancefromobject,
ct.customername, ct.email, ct.birthday,
ct.sharewithpublicasofdate, ct.sharewithresearchasofdate, ct.sharewithfriendsasofdate,
ct.lastupdatedate, ct.phone,
al.user, al.timestamp, al.x, al.y, al.z
FROM step_trainer_landing stl
INNER JOIN customer_trusted ct ON stl.serialnumber = ct.serialnumber
INNER JOIN accelerometer_trusted al ON stl.sensorreadingtime = al.timestamp;
'''
SQLQuery_node1733370275531 = sparkSqlQuery(glueContext, query = SqlQuery2962, mapping = {"customer_trusted":S3customer_trusted_node1733371437293, "step_trainer_landing":S3step_trainer_landing_node1733371480855, "accelerometer_trusted":S3accelerometer_trusted_node1733372684665}, transformation_ctx = "SQLQuery_node1733370275531")

# Script generated for node S3: step_trainer_curated
EvaluateDataQuality().process_rows(frame=SQLQuery_node1733370275531, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1733344472649", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
S3step_trainer_curated_node1733344718199 = glueContext.getSink(path="s3://stedi-hb-lake-house/step_trainer/curated/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="S3step_trainer_curated_node1733344718199")
S3step_trainer_curated_node1733344718199.setCatalogInfo(catalogDatabase="stedi-hb",catalogTableName="step_trainer_curated")
S3step_trainer_curated_node1733344718199.setFormat("json")
S3step_trainer_curated_node1733344718199.writeFrame(SQLQuery_node1733370275531)
job.commit()