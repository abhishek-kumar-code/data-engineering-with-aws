# Data Engineering with AWS

### <ins>List of Projects</ins>

| Module | Project Name |
| --- | --- |
| Automate Data Pipleines | [Data Pipelines with Airflow](#project-1-data-pipelines-with-airflow) | 
| Spark and Data Lakes | [STEDI Human Balance Analytics](#project-2-stedi-human-balance-analytics) |
| Cloud Data Warehouse | [Sparkify Cloud Data Warehouse in Redshift](#project-3-sparkify-cloud-data-warehouse-in-redshift) | 
| Data Modeling | [NoSQL Data Modeling with Apache Cassandra](#project-4-nosql-data-modeling-with-apache-cassandra) | 
_____
### <ins>Program Learning Outcomes</ins>  

* **Develop proficiency in Spark, Airflow, and Amazon Web Services tools.**
* **Automate and monitor production data pipelines.**
* **Build and interact with a cloud-based data lake.**
* **Work efficiently with massive datasets.**
* **Create scalable and efficient data warehouses in Cloud.**
* **Create user-friendly relational and NoSQL data models.**
_____
### <ins>Graduation Certificate</ins> 

![Create Table DAG](Certificate_Udacity_Original.jpg)

> [!NOTE]
> ###### _School of Data Science, Udacity Inc., Mountain View, CA. "Nanodegree" is a registered trademark of Udacity. © 2011-2024 Udacity, Inc._

> [!TIP]
> ###### _More information about this program can be found by visiting [Udacity Data Engineering Nanodegree](https://www.udacity.com/catalog)._
_____

# [Project 1: Data Pipelines with Airflow](./automate-data-pipelines-with-airflow)

## Objective: 

The objective of this project is to design and implement automated and monitored high grade data pipelines for Sparkify, a music streaming company, using Apache Airflow to enhance its data warehouse ETL processes. The main goals and requirements for the project are as follows:

**1. Automation and Monitoring**
- Implement automation in the ETL pipelines to streamline and enhance the data processing workflow.
- Ensure robust monitoring mechanisms to track the performance and health of the data pipelines.

**2. Dynamic and Reusable Data Pipelines**
- Design data pipelines that are dynamic, built from reusable tasks, and can be easily extended as needed.
- Incorporate functionality for easy backfills to accommodate historical data processing.

**3. Data Quality Assurance**
- Implement tests to validate data quality after the ETL steps have been executed.
- Ensure that any discrepancies in the datasets are detected and addressed before analyses are run on the DW.

**4. Data Integration**
- The source data, residing in S3, consists of JSON logs detailing user activity and JSON metadata about songs.
- Process and load the data into Sparkify's DW on Redshift, ensuring compatibility and efficient data flow.

## Airflow DAGs

**1. `final_project_create_table` DAG overview**

![Create Table DAG](automate-data-pipelines-with-airflow/images/final_project_create_table_DAG_Graph_Zoom.PNG)

**2. `final_project` DAG overview**

![Final Project DAG](automate-data-pipelines-with-airflow/images/final_project_DAG_Graph_Zoom.PNG)

## Datasets

Datasets for this project (S3 Links):

- **Log Data:**  
  `s3://udacity-dend/log_data`

- **Song Data:**  
  `s3://udacity-dend/song-data`

## Copy S3 Data

#### Step 1: Create a S3 Bucket using the AWS Cloudshell
```bash
aws s3 mb s3://akumar-dend/
```
#### Step 2: Copy Data from Udacity's S3 Bucket to Your CloudShell Directory
```bash
aws s3 cp s3://udacity-dend/log-data/ ~/log-data/ --recursive
aws s3 cp s3://udacity-dend/song-data/ ~/song-data/ --recursive
aws s3 cp s3://udacity-dend/log_json_path.json ~/
```
#### Step 3: Copy Data from Your CloudShell Directory to Your Own S3 Bucket
```bash
aws s3 cp ~/log-data/ s3://akumar-dend/log-data/ --recursive
aws s3 cp ~/song-data/ s3://akumar-dend/song-data/ --recursive
aws s3 cp ~/log_json_path.json s3://akumar-dend/
```
#### Step 4: Verify the Data is in Your S3 Bucket
```bash
aws s3 ls s3://akumar-dend/log-data/
aws s3 ls s3://akumar-dend/song-data/
aws s3 ls s3://akumar-dend/log_json_path.json
```

## AWS Redshift Serverless Configuration

#### Step 1: Create an IAM User (`awsuser`) in AWS

Create an IAM user named `awsuser` and assign the appropriate permissions.
- Attach the following policies to the IAM user:
  - _Administrator Access_
  - _AmazonRedshiftFullAccess_
  - _AmazonS3FullAccess_

#### Step 2: Create a Redshift Role (`redshift-dend`) via AWS CloudShell

- Attach the **AmazonS3FullAccess** policy to the role to provide full access to S3 using **AWS CloudShell**.
```bash
aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess --role-name redshift-dend
```

#### Step 3. Configure and Setup AWS Redshift Serverless

- Associate the IAM Role to establish a connection between Redshift Serverless and S3. 
- Configure Workgroup Settings:
  - Accept the default Workgroup settings.
  - Accept the defaults for Security and Encryption.
  - Enable Enhanced VPC Routing.
  - Add Inbound Rule to VPC Security Group associated with the Redshift cluste:
    - Type: Custom TCP
    - Port Range: 0 - 5500
    - Source: Anywhere-IPv4
    - Copy the Redshift Workgroup Endpoint (will be used later when configuring the Redshift connection in Airflow)

## Airflow Connection Configuration 

#### Step 1. Configure AWS Credentials Connection in Airflow

- Navigate to the **Airflow UI** and go to the **Connections** page. Click **Create** to add a new connection.
- On the **Create Connection** page, fill in the following values:
   - **Connection ID**: Enter `aws_credentials`
   - **Connection Type**: Choose `Amazon Web Services`
   - **AWS Access Key ID**: Enter the Access Key ID from the IAM User credentials you downloaded earlier.
   - **AWS Secret Access Key**: Enter the Secret Access Key from the IAM User credentials you downloaded earlier.
   - 
![aws_credentails](automate-data-pipelines-with-airflow/images/dend-aws_cred-iam-role.PNG)

#### Step 2. Configure Redshift Connection in Airflow

- Navigate to the **Airflow UI** and go to the **Connections** page. Click **Create** to add a new connection.
- On the **Create Connection** page, fill in the following values:
   - **Connection ID**: Enter `redshift`
   - **Connection Type**: Choose `Amazon Redshift`
   - **Host**: Enter the **endpoint** of your Redshift Serverless workgroup (excluding the port and schema name at the end). 
   - **Schema**: Enter `dev` (the Redshift database you want to connect to).
   - **Login**: Enter `awsuser` (the IAM user you created).
   - **Password**: Enter the password you set up when launching Redshift Serverless.
   - **Port**: Enter `5439` (the default Redshift port).

![aws_credentails](automate-data-pipelines-with-airflow/images/dend-redshift-serverless.PNG)

## Tasks, Operators & Task Depedencies

- `Begin_execution` and `Stop_execution`
  - Dummy operators representing DAG start and end point

- `Stage_events` and `Stage_songs`
  - The stage operator loads JSON-formatted files from S3 to Amazon Redshift. 

- `Load_songplays_fact_table` & `Load_*_dim_table`
  - Load and Transform data from staging to fact and dimension target tables

- `Data_quality_tests`
  - Data quality operator which runs checks on the data itself.
  - Functionality: To receive SQL based test cases along with the expected results and execute the tests.
  - Example: Run data quality checks to ensure no empty table.

![Task dependencies](automate-data-pipelines-with-airflow/images/Project_Workspace_sourcecode_operators_sqlstatements.PNG)

## DAG Execution

- DAG Dashboard

![Airflow Dashboard](automate-data-pipelines-with-airflow/images/airflow_DAGs_Dashboard.PNG)

- Trigger **`final_project_create_table`** DAG to create tables in Redshift

![Create Table DAG Grid](automate-data-pipelines-with-airflow/images/final_project_create_table_DAG_Grid.PNG)

- Run **`final_project`** DAG to trigger the ETL data pipeline

![Final Project DAG Grid](automate-data-pipelines-with-airflow/images/final_project_DAG_Grid.PNG)

_____

# [Project 2: STEDI Human Balance Analytics](./spark-and-data-lakes)

## Objective

This project involves building a **cloud-based data lakehouse solution** for sensor data collected by the STEDI Step Trainer and its mobile app to train a **machine learning model**. The solution will use: 
- **PySpark**: For processing large datasets.
- **AWS Glue**: Managed ETL for data preparation.
- **AWS Athena**: Serverless querying of data.
- **AWS S3**: Scalable storage for raw and processed data.
As a Data Engineer, you will extract and curate data from the **Step Trainer sensors** and the **mobile app** into the data lakehouse on AWS, enabling Data Scientists to train the model.

### STEDI Step Trainer Overview

The STEDI Step Trainer is a device designed to help users with balance exercises. It has the following features:

- **Sensors** detect motion and distance.
- The **mobile app** collects customer data and accelerometer data (X, Y, Z directions) for motion tracking.
- **Data Privacy Considerations**: Only data from **consenting customers** will be used for the machine learning model, ensuring privacy is prioritized.

## Lakehouse Architecture

The **Medallion Architecture** is a key feature of a **lakehouse architecture** that allows for the efficient ingestion and incremental improvement of data. This architecture organizes data into stages, each representing a different level of refinement. Each stage is symbolized by a color, similar to the medals in the Olympics.

![Image Alt Text](spark-and-data-lakes/images/lakehouse_architecture.png)

### Stages of Data Refinement

1. **Bronze (Raw Data)**: This is the initial stage where raw, unprocessed data is ingested into the lakehouse.
     - Data may contain errors, duplicates, or inconsistencies.
     - Minimal processing or transformation has been applied.
 
2. **Silver (Cleaned and Augmented Data)**: At this stage, the data undergoes filtering, cleaning, and augmentation to improve quality.
     - Errors and duplicates are removed.
     - Data is transformed to ensure consistency and standardization.

3. **Gold (Business-Level Aggregates)**: The final stage where data is aggregated to a business level, often using structures like **star schemas** for easy reporting and analytics.
     - Includes business-level aggregates, metrics, and KPIs.
     - Ready for consumption by business analysts or reporting tools.

## Datasets

STEDI provides three JSON data sources for use with the **Step Trainer**. These datasets are available in the following folders in the GitHub repository:

- **customer**
- **step_trainer**
- **accelerometer**

### 1. Customer Records: 
This dataset contains information from **fulfillment** and the **STEDI website**.
  - **AWS S3 Bucket URI**: `s3://cd0030bucket/customers/`

### 2. Step Trainer Records
This dataset includes data from the **motion sensor** on the Step Trainer device.
- **AWS S3 Bucket URI**: `s3://cd0030bucket/step_trainer/`

### 3. Accelerometer Records
This dataset contains data from the **mobile app’s accelerometer**.
- **AWS S3 Bucket URI**: `s3://cd0030bucket/accelerometer/`

## S3 Bucket Structure
On completion of this project, the S3 bucket should have the following directory structure:
```bash
customer/
- landing/
- trusted/
- curated/
accelerometer/
- landing/
- trusted/
step_trainer/
- landing/
- trusted/
- curated/
```

## Project Details

This project involves creating and managing **AWS Glue** tables for different datasets and performing data sanitization, validation, and aggregation tasks to support data analysis and machine learning model training.

#### High-Level Architecture

![Image Alt Text](spark-and-data-lakes/images/workflow_flowchart.PNG)

![Image Alt Text](spark-and-data-lakes/images/relationship_entities.PNG)

#### Stage 1: Create Glue Tables for Landing Zones

To get a feel for the data, you will create three Glue tables for the three landing zones. Query the tables using AWS Athena.

- `customer_landing.sql`
- `accelerometer_landing.sql`
- `step_trainer_landing.sql`

#### Stage 2: Create Spark Jobs for Sanitizing Customer and Accelerometer Data

The **Data Science team** has identified that the **Accelerometer Records** match **Customer Records**. You need to create two AWS Glue jobs to sanitize the data:

- **Job 1**: Sanitize **Customer Data** (from Website, Landing Zone).
  - Store **only customer records** that agreed to share their data for research purposes in a new Glue Table called `customer_trusted`.

- **Job 2**: Sanitize **Accelerometer Data** (from Mobile App, Landing Zone).
  - Store **only accelerometer readings** from customers who agreed to share their data for research purposes in a new Glue Table called `accelerometer_trusted`.

#### Stage 3: Create Spark Jobs to handle Data Quality Issue with Serial Numbers

A data quality issue exists where **Customer Records** in the **Landing Zone** contain duplicate serial numbers for many customers. However, **Step Trainer Records** contain the correct serial numbers.

- **Job 3**: Create a Spark job that sanitizes **Customer Data** (from Trusted Zone) and:
  - **Matches** customers with corresponding **Accelerometer Data**.
  - Creates a new Glue Table called `customers_curated`, containing **only customers who have accelerometer data** and agreed to share their data.

#### Stage 4: Create Spark Jobs to support further data processing

- **Job 4**: Step Trainer Trusted Data
  - Read the **Step Trainer IoT data stream** (S3) and populate a **Trusted Zone Glue Table** called `step_trainer_trusted`:
  - Only include data for customers who have **accelerometer data** and agreed to share their data for research purposes (from `customers_curated`).

- **Job 5**: Machine Learning Curated Data
  - Create an aggregated table that combines **Step Trainer Readings** and the corresponding **Accelerometer Readings**:
  - Match data based on the **same timestamp**.
  - Store this aggregated data in a Glue Table called `machine_learning_curated`:
    - Include only data from customers who agreed to share their data for research purposes.


## Data Validation

As part of the project, it is essential to validate the data at each stage to ensure the accuracy and completeness of the processed datasets. After completing each stage of the project, check the row count in the produced tables to confirm that they match the expected values.

### Expected Row Counts

#### 1. **Landing Zone**
   - **Customer**: 956 rows
   - **Accelerometer**: 81,273 rows
   - **Step Trainer**: 28,680 rows

#### 2. **Trusted Zone**
   - **Customer**: 482 rows
   - **Accelerometer**: 40,981 rows
   - **Step Trainer**: 14,460 rows

#### 3. **Curated Zone**
   - **Customer**: 482 rows
   - **Machine Learning**: 43,681 rows

## Final State and Results

### Landing Zone
Glue Table DDL scripts:

- [customer_landing.sql](spark-and-data-lakes/scripts/SQL%20DDL/customer_landing.sql)
- [accelerometer_landing.sql](spark-and-data-lakes/scripts/SQL%20DDL/accelerometer_landing.sql)
- [step_trainer_landing.sql](spark-and-data-lakes/scripts/SQL%20DDL/step_trainer_landing.sql)

**`customer_landing`** table output
![Image Alt Text](spark-and-data-lakes/images/Landing%20Zone/customer_landing.PNG)

**`accelerometer_landing`** table output
![Image Alt Text](spark-and-data-lakes/images/Landing%20Zone/accelerometer_landing.PNG)

**`step_trainer_landing`** table output
![Image Alt Text](spark-and-data-lakes/images/Landing%20Zone/step_trainer_landing.PNG)

Note: _AWS Athena images showing the customer landing data and accelerometer landing data_

### Trusted Zone
Spark Job Scripts:

- [customer_landing_to_trusted.py](spark-and-data-lakes/scripts/Spark%20Jobs/customer_landing_to_trusted.py)
- [accelerometer_landing_to_trusted_zone.py](spark-and-data-lakes/scripts/Spark%20Jobs/accelerometer_landing_to_trusted.py)
- [step_trainer_trusted.py](spark-and-data-lakes/scripts/Spark%20Jobs/step_trainer_trusted.py)

**`customer_trusted`** table output
![Image Alt Text](spark-and-data-lakes/images/Curated%20Zone/customer_trusted.PNG)

**`accelerometer_trusted`** table output
![Image Alt Text](spark-and-data-lakes/images/Curated%20Zone/accelerometer_trusted.PNG)

**`step_trainer_trusted`** table output
![Image Alt Text](spark-and-data-lakes/images/Curated%20Zone/step_trainer_trusted.PNG)

Note: _AWS Athena images showing the customer trusted data, accelerometer trusted and step trainer trusted data_

### Curated Zone
Spark Job Scripts:

- [customer_trusted_to_curated.py](spark-and-data-lakes/scripts/Spark%20Jobs/customer_trusted_to_curated.py)
- [machine_learning_curated.py](spark-and-data-lakes/scripts/Spark%20Jobs/machine_learning_curated.py)

**`customer_curated`** table output
![Image Alt Text](spark-and-data-lakes/images/Trusted%20Zone/customer_curated.PNG)

**`machine_learning_curated`** table output
![Image Alt Text](spark-and-data-lakes/images/Trusted%20Zone/machine_learning_curated.PNG) 

Note: _AWS Athena images showing the customer curated data and machine learning curated data_

# [Project 3: Sparkify Cloud Data Warehouse in Redshift](./cloud-data-warehouses)

## Project Overview
Sparkify is a growing music streaming startup with a large user base and song database. To scale and improve their operations, they have decided to migrate their data processing and storage to the cloud. As part of the project, they need an ETL pipeline to handle the extraction, transformation, and loading (ETL) of data stored in Amazon S3 into Amazon Redshift for analytics purposes.

The goal is to:

- **Extract** user activity and song metadata from S3.
- **Stage** the data in Redshift.
- **Transform** the data into a set of dimensional tables that the analytics team can use to gain insights into user behavior.

## High-Level Architecture

![Image Alt Text](cloud-data-warehouses/images/system_architecture.PNG) 

## Datasets
There are two primary datasets you will be working with:

- **Song Data**: Contains metadata about songs and their artists.
`s3://udacity-dend/song_data`
- **Log Data**: Contains simulated user activity logs from the Sparkify app.
`s3://udacity-dend/log_data`
- **Log JSON Metadata**: A JSON file specifying the structure of the log data for use in the ETL process.
`s3://udacity-dend/log_json_path.json`

#### Song Dataset
The Song Dataset is a subset of the Million Song Dataset, consisting of JSON files that contain metadata for songs and their artists. The dataset is partitioned by the first three characters of each song's track ID.

Example File Paths:

`song_data/A/B/C/TRABCEI128F424C983.json`
`song_data/A/A/B/TRAABJL12903CDCF1A.json`

**Sample JSON Structure:**
```bash
{
  "num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0
}
```

#### Log Dataset
The Log Dataset contains event logs generated by the app simulator based on user interactions with the songs. The log files are partitioned by year and month.

Example File Paths:

`log_data/2018/11/2018-11-12-events.json`
`log_data/2018/11/2018-11-13-events.json`

**Sample JSON Structure:**

```bash
{
  "artist": "Line Renaud", "auth": "Logged In", "firstName": "Jean", "gender": "M", "itemInSession": 0, "lastName": "Dupont", "length": 152.92, "level": "free", "location": "Paris, France",
  "method": "GET", "page": "Home", "registration": 1234567890, "sessionId":12345, "song": "Der Kleine Dompfaff", "status": 200, "ts": 1234567890, "userAgent": "Mozilla/5.0", "userId": 56789
}
```

#### Log JSON Metadata
The log_json_path.json file provides the structure for parsing the log data in Redshift. This file is essential for the COPY command when loading the log data from S3 into Redshift staging tables.

Purpose: Tells Redshift how to interpret the JSON data and extract relevant fields for transformation into analytics tables.
`s3://udacity-dend/log_json_path.json`

## AWS Configuration Instructions

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

## ETL Pipeline Instructions

1. Run **python create_tables.py** in terminal
```sh
home root$ python create_tables.py
```
- **Purpose:** This script will execute the SQL queries defined in _sql_queries.py_ to drop any existing tables and create the required tables for the ETL pipeline.
- **Tables Created:** Staging tables for raw data (staging_events, staging_songs), Fact table (songplays), and Dimension tables (users, songs, artists, time).

2. Run **python etl.py** in terminal 
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

![Image Alt Text](cloud-data-warehouses/images/staging_events.PNG) 
![Image Alt Text](cloud-data-warehouses/images/staging_songs.PNG) 

# [Project 4: NoSQL Data Modeling with Apache Cassandra](./data-modeling-with-apache-cassandra)

## Project Overview
Sparkify, a music streaming startup, wants to analyze the data collected from their app, specifically focusing on understanding which songs users are listening to. However, the current data stored in CSV files is not in an optimal format for querying and analysis. To solve this problem, Sparkify has tasked you with creating an Apache Cassandra database that will allow efficient querying on song play data.

Your role as a data engineer is to:

Design a database schema in Apache Cassandra for querying song play data.
Implement an ETL (Extract, Transform, Load) pipeline to process data from CSV files into the Cassandra database.
Test the database with specific queries provided by the analytics team to ensure the schema supports the necessary analysis.

## Objective
The main objective of this project is to create a data model using Apache Cassandra and set up an ETL pipeline using Python. You will need to:

Model the data to create tables in Apache Cassandra that support the required queries.
Process the data by transforming raw CSV files into a streamlined format for insertion into Cassandra.
Test the database by running queries provided by the analytics team to validate the design and results.

## Project Files
This project consists of the following files:

- event_data - This is all the data collected on songs and user activity on Sparkfy new music streaming app.
- Project_1B_ Project_Template.ipynb - This file contains the Database and ETL code.
- event_datafile_new.csv - This csv file denormalised from event_data file that will be used to insert data into the Apache Cassandra tables.
- images - A screenshot of the data in the event_datafile_new.csv

## Project Execution
Run Project_1B_ Project_Template.ipynb to run validation and example queries.
![Image Alt Text](data-modeling-with-apache-cassandra/home/images/jupyter_notebook.PNG) 
