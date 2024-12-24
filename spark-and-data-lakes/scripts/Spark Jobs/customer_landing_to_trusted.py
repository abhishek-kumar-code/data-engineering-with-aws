import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality
import re

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

# Script generated for node S3 Bucket Landing Zone
S3BucketLandingZone_node1733267579959 = glueContext.create_dynamic_frame.from_options(format_options={"multiLine": "false"}, connection_type="s3", format="json", connection_options={"paths": ["s3://stedi-hb-lake-house/customer/landing/"], "recurse": True}, transformation_ctx="S3BucketLandingZone_node1733267579959")

# Script generated for node Privacy Filter
PrivacyFilter_node1733267636312 = Filter.apply(frame=S3BucketLandingZone_node1733267579959, f=lambda row: (not(row["shareWithResearchAsOfDate"] == 0)), transformation_ctx="PrivacyFilter_node1733267636312")

# Script generated for node Trusted Customer Zone
EvaluateDataQuality().process_rows(frame=PrivacyFilter_node1733267636312, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1733267493488", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
TrustedCustomerZone_node1733267643618 = glueContext.getSink(path="s3://stedi-hb-lake-house/customer/trusted/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], compression="gzip", enableUpdateCatalog=True, transformation_ctx="TrustedCustomerZone_node1733267643618")
TrustedCustomerZone_node1733267643618.setCatalogInfo(catalogDatabase="stedi-hb",catalogTableName="customer_trusted")
TrustedCustomerZone_node1733267643618.setFormat("json")
TrustedCustomerZone_node1733267643618.writeFrame(PrivacyFilter_node1733267636312)
job.commit()