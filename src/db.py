# db.py
import psycopg2

def get_conn():
    return psycopg2.connect(
        host="localhost",
        user="postgres",
        password="angrybirds",
        database="Hotel"
    )
