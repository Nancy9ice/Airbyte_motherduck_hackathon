import pandas as pd
import logging
import mysql.connector
from db_conn import get_mysql_conn
import pyodbc
import time


# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def execute_sql(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    
    if not results:  # Check if the results are empty
        query_results = pd.DataFrame(columns=[desc[0] for desc in cursor.description])
    else:
        query_results = pd.DataFrame([list(i) for i in results], 
                                     columns=[desc[0] for desc in cursor.description])
    
    cursor.close()
    return query_results


def execute_sql_with_retry(connection, query, retries=3, delay=2):
    last_exception = None  # Store the last exception encountered
    
    for attempt in range(retries):
        try:
            # Try executing the SQL query
            return execute_sql(connection, query)
        except (mysql.connector.Error, pyodbc.Error) as e:
            last_exception = e  # Save the exception
            
            if attempt < retries - 1:
                # Log a warning and retry if not the last attempt
                logger.warning(f"Warning: OperationalError on attempt {attempt + 1}/{retries}: {e}")
                logger.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
                
                # Attempt reconnection
                try:
                    if isinstance(connection, mysql.connector.MySQLConnection):
                        connection.reconnect(attempts=3, delay=2)
                    elif isinstance(connection, pyodbc.Connection):
                        connection.close()
                        connection = pyodbc.connect(connection.getinfo(pyodbc.SQL_CONNECTION_STRING))
                except Exception as reconnection_error:
                    # Log a warning but don't raise the exception to allow for further retries
                    logger.warning(f"Reconnection failed on attempt {attempt + 1}/{retries}: {reconnection_error}")
            else:
                # If it's the last attempt, log the final error and raise
                logger.error(f"Max retries reached, query failed. Final error: {last_exception}")
    
    # If all retries fail, raise the last captured exception
    raise last_exception



def split_and_execute_queries(conn, query_file_path):
    with open(query_file_path, 'r') as file:
        query = file.read()
        query_results = execute_sql_with_retry(conn, query)

    return query_results


# results = split_and_execute_queries(get_mysql_conn(), 'sql_query.sql')
# results2 = results[results["exam_year"] == 2019]
# print(results2)