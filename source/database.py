import psycopg2
from config import Settings
from psycopg2 import pool

DB_CONNECTION_CONFIG = {
    "database": Settings.POSTGRES_DB,
    "user": Settings.POSTGRES_USER,
    "password": Settings.POSTGRES_PASSWORD,
    "host": Settings.POSTGRES_HOST,
    "port": Settings.POSTGRES_PORT,
}

# with psycopg2.connect(** DB_ARGUMENTS) as DB_conn:
#     with conn.cursor() as cursor:

connection_pool = psycopg2.pool.SimpleConnectionPool(1, 10, **DB_CONNECTION_CONFIG)


def get_connection():
    return connection_pool.getconn()


def release_connection(db_connection):
    connection_pool.putconn(db_connection)


def close_pool():
    connection_pool.closeall()
