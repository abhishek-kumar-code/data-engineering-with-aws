# Importing necessary libraries
# For reading the configuration file (dwh.cfg)
# For connecting to the PostgreSQL/Redshift database
# Importing the SQL queries from a separate file (sql_queries)
import configparser  
import psycopg2  
from sql_queries import drop_table_queries, create_table_queries  

# Function to drop existing tables in the Redshift database
def drop_tables(cur, conn):
    """
    This function takes in the cursor (cur) and connection (conn) objects and 
    executes the DROP TABLE queries defined in 'drop_table_queries' to remove
    any existing tables before creating new ones.
    """
    for query in drop_table_queries:
        # Execute the drop query
        cur.execute(query)
        # Commit the transaction to apply the changes in the database
        conn.commit()  

# Function to create the tables in the Redshift database
def create_tables(cur, conn):
    """
    This function takes in the cursor (cur) and connection (conn) objects and 
    executes the CREATE TABLE queries defined in 'create_table_queries'.
    These queries create the staging, fact, and dimension tables in Redshift.
    """
    for query in create_table_queries:
        # Execute the create query for each table
        cur.execute(query)  
        # Commit the transaction to apply the changes in the database
        conn.commit()  

# Main function to connect to Redshift and execute the table operations
def main():
    """
    Main function that:
    1. Reads the configuration file (dwh.cfg) to fetch necessary credentials.
    2. Establishes a connection to Redshift using psycopg2.
    3. Drops existing tables using the drop_tables function.
    4. Creates the necessary tables using the create_tables function.
    5. Closes the connection to the database after completing the operations.
    """
    # Reading the configuration file ('dwh.cfg') to get credentials for the Redshift cluster
    config = configparser.ConfigParser()
    # Reads the config file that contains cluster, database, user, password, etc.
    config.read('dwh.cfg')  

    # Establishing connection to the Redshift database using the credentials from the config file
    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    # Creating a cursor object to interact with the database
    cur = conn.cursor()  

    # Drop existing tables (if any) and create the necessary tables
    # Drop tables using predefined SQL queries in 'drop_table_queries'
    drop_tables(cur, conn)  
    # Create tables using predefined SQL queries in 'create_table_queries'
    create_tables(cur, conn)  

    # Close the database connection once all operations are done
    conn.close()

# Checking if the script is being run directly, and if so, calling the main function
if __name__ == "__main__":
    main()
