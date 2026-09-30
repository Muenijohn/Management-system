import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

try:
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="38515646",  # Put your postgres password here
        host="localhost",
        port=5432
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute("CREATE DATABASE school_supplies_db;")
    print("Database 'school_supplies_db' created successfully!")
    cur.close()
    conn.close()
except psycopg2.errors.DuplicateDatabase:
    print("Database 'school_supplies_db' already exists! You are good to go.")
except Exception as e:
    print(f"Error: {e}")