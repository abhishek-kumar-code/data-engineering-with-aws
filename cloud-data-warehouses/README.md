### Cloud Data Warehouses

_This document provides the step-by-step instructions for setting up and running the ETL pipeline and configuring necessary AWS resources to support the Redshift data warehouse._

#### [A] ETL Pipeline Instructions
(i) Run python create_tables.py in terminal
```sh
home root$ python create_tables.py
```
- **Purpose:** This script will execute the SQL queries defined in _sql_queries.py_ to drop any existing tables and create the required tables for the ETL pipeline.
- **Tables Created:** Staging tables for raw data (staging_events, staging_songs), Fact table (songplays), and Dimension tables (users, songs, artists, time).

(ii) Run python etl.py in terminal 
```sh
home root$ python etl.py
```
To Complete the ETL Process: After the tables are set up, you will run the ETL process that loads data from S3 into Redshift and transforms it into a star-schema format for song play analysis.

- **Purpose:**: This script will load raw data from Amazon S3 into the Redshift staging tables using the COPY command (staging_events and staging_songs). It will also transform data from the staging tables into the final star-schema Fact and Dimension tables for song play analysis.
- **Tables Created:**- Fact Table, Dimension Tables.

| Table Type | Table Name |
| ------ | ------ |
| Fact Table | songplays |
| Dimension Table | users |
| Dimension Table | songs |
| Dimension Table | artists |
| Dimension Table | time |

**Note:** 
- The data is stored in the S3 buckets configured in the dwh.cfg file.
- All SQL queries are stored in sql_queries.py, and queries for verifying the data ingestion and ETL process are available in the images/ directory.

After the data is loaded and transformed into these tables, it will be available for querying in Redshift for further analysis.

#### [B] AWS Configuration Instructions

_To set up the necessary resources on AWS for supporting the Redshift data warehouse, follow these steps:_

##### 1. Create an IAM Role

- Log in to the AWS Management Console and navigate to the IAM (Identity and Access Management) section.
- Create an IAM Role with the following settings:
-- Policy: Attach the AmazonS3ReadOnlyAccess policy. This gives Redshift the permission to read data from S3 buckets
- Trust Relationship: Set the trust relationship to allow the Redshift service to assume this role.
**Role Name:** _myRedshiftRole_



##### 2. Create a Security Group for Redshift
_In the AWS Management Console, go to the VPC section_
- Create a security group called _redshift_security_group_ that allows inbound and outbound access to/from Redshift.
- Configure the security group to allow traffic on port 5439, which is the default port for Redshift.

##### 3. Create an IAM User for Redshift
_In IAM, create a new IAM user with the username awsuser-redshift_
- Attach the following two policies to the IAM user:
-- **AmazonRedshiftFullAccess**: This policy grants the IAM user full access to Redshift resources.
-- **AmazonS3ReadOnlyAccess**: This policy grants read-only access to S3 resources.
- After creating the IAM user, generate and save the Access Key ID and Secret Access Key for future reference. These will be used to authenticate the connection to Redshift from your Python scripts.

##### 4. Launch a Redshift Cluster
_In the AWS Management Console, go to the Redshift service_
- Create a new Redshift cluster (redshift-cluster-1) and attach the following:.
- Subnet Group: Create a subnet group for the Redshift cluster if not already present.
- IAM Role: Attach the myRedshiftRole IAM role created earlier.
- Security Group: Attach the _redshift_security_group_ security group.
- Configure other settings for the Redshift cluster as needed, such as the database name, port, and cluster type.

After the cluster is launched, you can connect to it using the provided endpoint and credentials (username and password).

