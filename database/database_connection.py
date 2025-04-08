import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("HOST")
DATABASE = os.getenv("DATABASE")
USER = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

def get_database_connection():
    """Create a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            host=HOST,  
            database=DATABASE,
            user=USER,
            password=PASSWORD,
        )

        print("Connected to the database")    
        return conn
    
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None
