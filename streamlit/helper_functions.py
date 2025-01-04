from dotenv import load_dotenv
import os
import duckdb

# Load environment variables from a .env file
load_dotenv()

def create_connection():
    """
    Establishes a connection to the DuckDB database.
    """
    # Retrieve the MotherDuck token from environment variables
    motherduck_token = os.environ.get('MOTHERDUCK_TOKEN')
    
    if not motherduck_token:
        raise ValueError("MOTHERDUCK_TOKEN is not set in the environment variables.")
    
    # Construct the connection string with the token
    connection_string = f"md:Airbyte_Motherduck_Hackathon?motherduck_token={motherduck_token}"
    
    # Establish and return the connection
    conn = duckdb.connect(database=connection_string)
    return conn


def query_table_to_df(conn, schema_name, table_name):
    """
    Queries all records from the specified table within a schema and returns the results as a Pandas DataFrame.

    Parameters:
    conn (duckdb.DuckDBPyConnection): The database connection object.
    schema_name (str): The name of the schema containing the table.
    table_name (str): The name of the table to query.

    Returns:
    pd.DataFrame: Query results as a Pandas DataFrame.
    """
    # Validate schema and table names
    if not (schema_name.isidentifier() and table_name.isidentifier()):
        raise ValueError("Invalid schema or table name provided.")

    # Construct the fully qualified table name
    qualified_table_name = f'"{schema_name}"."{table_name}"'

    # Construct the SQL query
    query = f'SELECT * FROM {qualified_table_name} LIMIT 1000000'

    # Execute the query and fetch results as a DataFrame
    df = conn.execute(query).df()
    return df