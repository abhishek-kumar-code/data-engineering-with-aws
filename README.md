# Data Engineering with AWS

### Nanodegree Project
| Sl.No. | Project Name| Description | Tech Stack |
| --- | --- | --- | --- |
| Automate Data Pipleines with Airflow  | [Project 1: Data Pipelines with Airflow](./automate-data-pipelines-with-airflow) |
| git diff | Show file differences that haven't been staged |
| git status | List all new or modified files |
| git diff | Show file differences that haven't been staged |

#### > [Project 1: Data Pipelines with Airflow](./automate-data-pipelines-with-airflow)
#### > [Project 1: Data Pipelines with Airflow](./automate-data-pipelines-with-airflow)
#### [Project 1: Data Pipelines with Airflow](./automate-data-pipelines-with-airflow)
#### [Project 1: Data Pipelines with Airflow](./automate-data-pipelines-with-airflow)

### <ins>Program Learning Outcomes</ins>  

* **Develop proficiency in Spark, Airflow, and Amazon Web Services tools.**
* **Automate and monitor production data pipelines.**
* **Build and interact with a cloud-based data lake.**
* **Work efficiently with massive datasets.**
* **Create scalable and efficient data warehouses in Cloud.**
* **Create user-friendly relational and NoSQL data models.**
___

## [Project 1: Data Pipelines with Airflow](./automate-data-pipelines-with-airflow)

### Objective: 

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

For this project, you'll be working with two datasets. Here are the S3 links for each:

- **Log Data:**  
  `s3://udacity-dend/log_data`

- **Song Data:**  
  `s3://udacity-dend/song-data`

## Copy S3 Data

#### Step 1: Create a S3 Bucket using the AWS Cloudshell
```bash
aws s3 mb s3://akumar-dend/`
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
aws s3 ls s3://your-unique-bucket-name/log-data/
aws s3 ls s3://your-unique-bucket-name/song-data/
aws s3 ls s3://your-unique-bucket-name/log_json_path.json
```
### AWS Redshift Serverless Configuration 
1. Create an IAM User awsuser in AWS
Permissions - attach exiting policies:

Administrator Access
AmazonRedshiftFullAccess
AmazonS3Full Access

Create a Redshift Role called redshift-dend from the AWS Cloudshell
Now, provide the my-redshift-service-role with full access to S3:
aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess --role-name my-redshift-service-role


2. Configure AWS Redshift Serverless
Create a Redshift Role my-redshift-service-role from the AWS Cloudshell
Click on Associate IAM role, and choose the my-redshift-service-role created through the AWS CloudShell. Afterward, click Associate IAM roles. This action enables Redshift Serverless to establish a connection with S3.

Give the role S3 Full Access

aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess --role-name my-redshift-service-role
Setup AWS Redshift Serverless

Copy and store the Redshift Workgroup endpoint locally, we will need this while configuring Airflow (redshift connection)
### Airflow Setup
3. Configure Connections in Airflow UI
Add Airflow Connections:

Connection ID: aws_credentails, Connetion Type: Amazon Web Services

![aws_credentails](automate-data-pipelines-with-airflow/images/dend-aws_cred-iam-role.PNG)

Connection ID: redshift, Connetion Type: Amazon Redshift

![aws_credentails](automate-data-pipelines-with-airflow/images/dend-redshift-serverless.PNG)

4. Configure Variables in Airflow UI - S3 Paths
Key = s3_bucket
Value = akumar-dend (bucket name)
### Operators

Begin_execution & Stop_execution

Dummy operators representing DAG start and end point

Stage_events & Stage_songs

Extract and Load data from S3 to Amazon Redshift

Load_songplays_fact_table & Load_*_dim_table

Load and Transform data from staging to fact and dimension tables

Run_data_quality_checks

![Task dependencies](automate-data-pipelines-with-airflow/images/Project_Workspace_sourcecode_operators_sqlstatements.PNG)
Run data quality checks to ensure no empty tables
### DAG Execution
Trigger final_project_create_table DAG to create tables in Redshift

![Airflow Dashboard](automate-data-pipelines-with-airflow/images/airflow_DAGs_Dashboard.PNG)

Trigger final_project_create_table DAG to create tables in Redshift

![Create Table DAG Grid](automate-data-pipelines-with-airflow/images/final_project_create_table_DAG_Grid.PNG)

Run final_project DAG to trigger the ETL data pipeline

![Final Project DAG Grid](automate-data-pipelines-with-airflow/images/final_project_DAG_Grid.PNG)
   
### Order of Execution 
1. Copy S3 data from Udacity Bucket to Cloudshell --> Datasets and Copy S3 Data
2. Copy data from home cloudshell directory to akumar-dend (my S3 bucket)
3. Configure AWS Redshift Serverless (as per Lesson#3.12)
4. Add Airflow Connections to AWS Redshift (as per Lesson#3.13 - see images folder for connection)
5. Add Airflow User Setup (as per Lesson#3.5 - - see images folder for connection)
6. Run final_project_create_table DAG (create_redshift_tables.py) to trigger create tables in Redshift
7. Run final_project DAG (final_project.py) to trigger the data pipeline

> [!NOTE]
> School of Data Science, Udacity. Program curricula attached below.
[Program Syllabus](./Data%2BEngineering%2BNanodegree%2BProgram%2BSyllabus.pdf), more information about this program can be found by visiting [Udacity Data Engineering ND](https://www.udacity.com/course/data-engineer-nanodegree--nd027).
