import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

conn = psycopg2.connect(user="postgres", password="Bhavya@380", host="localhost", port="5432", database="postgres")
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = conn.cursor()
cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'crms_db'")
exists = cursor.fetchone()
if not exists:
    cursor.execute("CREATE DATABASE crms_db")
    print("Database 'crms_db' created perfectly!")
else:
    print("Database 'crms_db' already exists.")
cursor.close()
conn.close()
