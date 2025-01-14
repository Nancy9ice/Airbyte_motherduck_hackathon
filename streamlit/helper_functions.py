from dotenv import load_dotenv
import os
import duckdb
import streamlit as st
import pandas as pd

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


@st.cache_data
def fetch_data():
    """Fetch data from Motherduck."""
    try:
        conn = create_connection()

        # Query the table and get the results as a DataFrame
        df = query_table_to_df(conn, 'exposures', 'waec_performance_metrics')
        df2a = query_table_to_df(conn, 'exposures', 'sat_performance_metrics')
        df2b = query_table_to_df(conn, 'main', 'sat_pred_recommendations')

        df2 = pd.merge(df2a, df2b, left_on='student_id', right_on='Student ID', how='left')
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error
    finally:
        if conn:
            conn.close()
    return df, df2