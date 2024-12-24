# Importing necessary libraries
# Used for reading the configuration file (dwh.cfg)
import configparser  
# Used for connecting to the PostgreSQL/Redshift database
import psycopg2 
# Importing SQL queries for copying and inserting data
from sql_queries import copy_table_queries, insert_table_queries  

# Function to load data from S3 into Redshift staging tables
def load_staging_tables(cur, conn):
    """
    This function takes a cursor (cur) and connection (conn) to execute 
    COPY commands that load data from S3 into the staging tables in Redshift.
    The COPY queries are stored in the 'copy_table_queries' list imported from 
    the sql_queries.py file.
    """
    # Iterate over each COPY query
    for query in copy_table_queries:  
        # Optional: Prints the query for logging or debugging purposes
        print(query)  
        # Executes the COPY query to load data into staging tables
        cur.execute(query)  
        # Commits the transaction to make sure the data is loaded into Redshift
        conn.commit()  

# Function to insert data into analytics tables (fact and dimension tables)
def insert_tables(cur, conn):
    """
    This function takes a cursor (cur) and connection (conn) to execute 
    INSERT INTO commands that move data from staging tables into the final 
    analytics tables (fact and dimension tables) in Redshift.
    The INSERT queries are stored in the 'insert_table_queries' list imported from 
    the sql_queries.py file.
    """
    # Iterate over each INSERT query
    for query in insert_table_queries:  
        # Executes the INSERT query to move data into analytics tables
        cur.execute(query)  
        # Commits the transaction to ensure the data is inserted into the tables
        conn.commit()  

# Main function that orchestrates the loading and inserting processes
def main():
    """
    Main function to:
    1. Read the configuration file ('dwh.cfg') for database connection parameters.
    2. Establish a connection to Redshift using psycopg2.
    3. Call the load_staging_tables() function to load data into staging tables.
    4. Call the insert_tables() function to insert data into the final analytics tables.
    5. Close the connection to Redshift.
    """
    # Reading the configuration file to extract necessary connection details for Redshift
    config = configparser.ConfigParser()
    # Reads the config file containing credentials for the Redshift cluster
    config.read('dwh.cfg')  

    # Establishing the connection to the Redshift cluster using the provided credentials
    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    # Creating a cursor object to interact with the database
    cur = conn.cursor()  

    # Load data into staging tables from S3
    # Call the function to load data into staging tables
    load_staging_tables(cur, conn)  

    # Insert data from staging tables into final analytics tables (fact and dimension tables)
    # Call the function to move data into analytics tables
    insert_tables(cur, conn)  

    # Close the database connection after completing the operations
    conn.close()

# Ensures the main() function is executed only if the script is run directly (not imported)
if __name__ == "__main__":
    main()
