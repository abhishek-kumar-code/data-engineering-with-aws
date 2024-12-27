# Data Engineering with AWS

### <ins>List of Projects</ins>

| Module | Project Name| Description | Tech Stack |
| --- | --- | --- | --- |
| Automate Data Pipleines | [Data Pipelines with Airflow](./automate-data-pipelines-with-airflow) | [Project 1: Data Pipelines with Airflow](./automate-data-pipelines-with-airflow) | Apache Airflow |
| Spark and Data Lakes | [STEDI Human Balance Analytics](./automate-data-pipelines-with-airflow) | [Project 1: Data Pipelines with Airflow](./automate-data-pipelines-with-airflow) | Apache Airflow |
| Cloud Data Warehouse | [Sparkify Cloud Data Warehouse in Redshift](./automate-data-pipelines-with-airflow) | [Project 1: Data Pipelines with Airflow](./automate-data-pipelines-with-airflow) | Apache Airflow |
| Data Modeling | [NoSQL Data Modeling with Apache Cassandra](./automate-data-pipelines-with-airflow) | [Project 1: Data Pipelines with Airflow](./automate-data-pipelines-with-airflow) | Apache Airflow |
_____
### <ins>Program Learning Outcomes</ins>  

* **Develop proficiency in Spark, Airflow, and Amazon Web Services tools.**
* **Automate and monitor production data pipelines.**
* **Build and interact with a cloud-based data lake.**
* **Work efficiently with massive datasets.**
* **Create scalable and efficient data warehouses in Cloud.**
* **Create user-friendly relational and NoSQL data models.**

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

## AWS Redshift Serverless Configuration Guide


#### 1. Create an IAM User (`awsuser`) in AWS

Create an IAM user named `awsuser` and assign the appropriate permissions.
- Attach the following policies to the IAM user:
  - _Administrator Access_
  - _AmazonRedshiftFullAccess_
  - _AmazonS3FullAccess_
These policies ensure the user has the necessary permissions to manage Redshift, S3, and perform administrative tasks.

#### 2. Create a Redshift Role (`redshift-dend`) via AWS CloudShell
- Open **AWS CloudShell**.
  - Attach the **AmazonS3FullAccess** policy to the role to provide full access to S3.
```bash
aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess --role-name my-redshift-service-role
```
#### 3. Configure and Setup AWS Redshift Serverless
-Create a Redshift Role (my-redshift-service-role) in AWS CloudShell.
-Associate the IAM Role:
  - Navigate to the Redshift Serverless console.
  - Under IAM Role, click on Associate IAM Role.
  - Select the my-redshift-service-role that was created in AWS CloudShell.
  - Click Associate IAM Roles. This action enables Redshift Serverless to establish a connection with S3.
  - Grant S3 Full Access to the my-redshift-service-role:
```bash
aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess --role-name my-redshift-service-role
```
Configure Workgroup Settings:

Accept the default Workgroup settings.
Accept the defaults for Security and Encryption.
Enable Enhanced VPC Routing:

Ensure that Enhanced VPC Routing is turned on for better network performance.
Add Inbound Rule to VPC Security Group:

Go to the VPC Security Group associated with your Redshift cluster.
Add an Inbound Rule:
Type: Custom TCP
Port Range: 0 - 5500
Source: Anywhere-IPv4
Copy the Redshift Workgroup Endpoint:

Copy the Redshift Workgroup endpoint and store it locally. This endpoint will be used later when configuring the Redshift connection in Airflow.

### AWS Redshift Serverless Configuration 
1. Create an IAM User awsuser in AWS
Permissions - attach exiting policies:

Administrator Access
AmazonRedshiftFullAccess
AmazonS3Full Access

2. Create a Redshift Role called redshift-dend from the AWS Cloudshell
Now, provide the my-redshift-service-role with full access to S3:
aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess --role-name my-redshift-service-role


3. Configure and Setup AWS Redshift Serverless
Create a Redshift Role my-redshift-service-role from the AWS Cloudshell
Click on Associate IAM role, and choose the my-redshift-service-role created through the AWS CloudShell. Afterward, click Associate IAM roles. This action enables Redshift Serverless to establish a connection with S3.

Give the role S3 Full Access.
aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess --role-name my-redshift-service-role

Accept the default Workgroup settings. 
Accept the defaults for Security and encryption.
Turn on enhanced VPC routing 
Add an inbound rule, under VPC security group.
Type = Custom TCP
Port range = 0 - 5500
Source = Anywhere-iPv4
Copy and store the Redshift Workgroup endpoint locally, we will need this while configuring Airflow (redshift connection)

# Airflow Connection Configuration Guide

This guide provides step-by-step instructions to configure connections in the Airflow UI for integrating AWS and Amazon Redshift.

---

## **1. Configure AWS Credentials Connection**

To set up an AWS connection in Airflow, follow the steps below.

### **Connection Details:**
- **Connection ID**: `aws_credentials`
- **Connection Type**: Amazon Web Services

### **Steps:**
1. Navigate to the **Airflow UI** and go to the **Connections** page.
2. Click **Create** to add a new connection.
3. On the **Create Connection** page, fill in the following values:
   - **Connection ID**: Enter `aws_credentials`
   - **Connection Type**: Choose `Amazon Web Services`
   - **AWS Access Key ID**: Enter the Access Key ID from the IAM User credentials you downloaded earlier.
   - **AWS Secret Access Key**: Enter the Secret Access Key from the IAM User credentials you downloaded earlier.
4. Once you’ve entered the necessary values, click **Save** to complete the configuration.
![aws_credentails](automate-data-pipelines-with-airflow/images/dend-aws_cred-iam-role.PNG)
---

## **2. Configure Redshift Connection**

To set up a Redshift connection in Airflow, follow the instructions below.

### **Connection Details:**
- **Connection ID**: `redshift`
- **Connection Type**: Amazon Redshift

### **Steps:**
1. Navigate to the **Airflow UI** and go to the **Connections** page.
2. Click **Create** to add a new connection.
3. On the **Create Connection** page, fill in the following values:
   - **Connection ID**: Enter `redshift`
   - **Connection Type**: Choose `Amazon Redshift`
   - **Host**: Enter the **endpoint** of your Redshift Serverless workgroup (excluding the port and schema name at the end). You can find this by selecting your workgroup in the Amazon Redshift console.
     - **IMPORTANT**: Do not include the port and schema name in the endpoint string.
   - **Schema**: Enter `dev` (the Redshift database you want to connect to).
   - **Login**: Enter `awsuser` (the IAM user you created).
   - **Password**: Enter the password you set up when launching Redshift Serverless.
   - **Port**: Enter `5439` (the default Redshift port).
4. Once you’ve entered the necessary values, click **Save** to complete the configuration.
![aws_credentails](automate-data-pipelines-with-airflow/images/dend-redshift-serverless.PNG)


### Airflow Setup
3. Configure Connections in Airflow UI
Add Airflow Connections:

Connection ID: aws_credentails, Connetion Type: Amazon Web Services

On the create connection page, enter the following values:
Connection Id: Enter aws_credentials.
Connection Type: Enter Amazon Web Services.
AWS Access Key ID: Enter your Access key ID from the IAM User credentials you downloaded earlier.
AWS Secret Access Key: Enter your Secret access key from the IAM User credentials you downloaded earlier. Once you've entered these values, select Save.

![aws_credentails](automate-data-pipelines-with-airflow/images/dend-aws_cred-iam-role.PNG)

Connection ID: redshift, Connetion Type: Amazon Redshift

On the Airflow create connection page, enter the following values:

Connection Id: Enter redshift.
Connection Type: Choose Amazon Redshift.
Host: Enter the endpoint of your Redshift Serverless workgroup, excluding the port and schema name at the end. You can find this by selecting your workgroup in the Amazon Redshift console. See where this is located in the screenshot below. IMPORTANT: Make sure to NOT include the port and schema name at the end of the Redshift endpoint string.
Schema: Enter dev. This is the Redshift database you want to connect to.
Login: Enter awsuser.
Password: Enter the password you created when launching Redshift serverless.
Port: Enter 5439. Once you've entered these values, select Save.

![aws_credentails](automate-data-pipelines-with-airflow/images/dend-redshift-serverless.PNG)

4. Configure Variables in Airflow UI - S3 Paths
Key = s3_bucket
Value = akumar-dend (bucket name)

### Operators

Begin_execution and Stop_execution

Dummy operators representing DAG start and end point

Stage_events and Stage_songs

The stage operator loads JSON-formatted files from S3 to Amazon Redshift. 

Load_songplays_fact_table & Load_*_dim_table

Load and Transform data from staging to fact and dimension target tables

Data_quality_tests

The final operator to create is the data quality operator, which runs checks on the data itself. The operator's main functionality is to receive one or more SQL based test cases along with the expected results and execute the tests.

![Task dependencies](automate-data-pipelines-with-airflow/images/Project_Workspace_sourcecode_operators_sqlstatements.PNG)
Run data quality checks to ensure no empty tables

### DAG Execution
Trigger final_project_create_table DAG to create tables in Redshift

![Airflow Dashboard](automate-data-pipelines-with-airflow/images/airflow_DAGs_Dashboard.PNG)

Trigger final_project_create_table DAG to create tables in Redshift

![Create Table DAG Grid](automate-data-pipelines-with-airflow/images/final_project_create_table_DAG_Grid.PNG)

Run final_project DAG to trigger the ETL data pipeline

![Final Project DAG Grid](automate-data-pipelines-with-airflow/images/final_project_DAG_Grid.PNG)
   

