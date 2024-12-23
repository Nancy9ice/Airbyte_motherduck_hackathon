import mysql.connector
from mysql.connector import Error
import os

from dotenv import load_dotenv 

load_dotenv()

def get_mysql_conn(timeout=250):
    try:
        conn = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST'),
            port=os.getenv('MYSQL_PORT'),
            database=os.getenv('MYSQL_DATABASE'),
            user=os.getenv('MYSQL_USERNAME'),
            password=os.getenv('MYSQL_PASSWORD'),
            connect_timeout=timeout
        )
        if conn.is_connected():
            print('Database Connection successful')
            return conn
    except Error as e:
        print(f"Error: {e}")