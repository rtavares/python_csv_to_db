import contextlib
import logging
from pathlib import Path

import pandas as pd
import psycopg2
from config import Settings
from data_models import BOOK_TABLE_FIELDS
from database import close_pool, get_connection, release_connection

settings = Settings()
settings.setup_logging()

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / f"books_data/{settings.INPUT_FILE}"


def process_db_data(
    sql_command: str = None, data: list | None = None, executemany: bool = False
) -> psycopg2.extensions.cursor | None:
    if sql_command is None:
        raise ValueError("sql_command is required")

    logger.info("Acquiring DB CONN at get_data()")
    db_connection = get_connection()
    logger.info(f"db_connection: {db_connection}")

    try:
        with contextlib.closing(db_connection.cursor()) as cursor:
            if executemany:
                cursor.executemany(sql_command, data)
                logger.info(f"Execute many SQL command: {sql_command}")
            else:
                cursor.execute(sql_command)
                logger.info(f"Execute single SQL command: {sql_command}")
            db_connection.commit()
            return cursor
    except psycopg2.Error as e:
        logger.error(f"Error while accessing PostgreSQL: {e}")
    finally:
        logger.info("Closing connection")
        release_connection(db_connection)


def insert_data_from_df_to_db(
    table_name: str = None, dataset: pd.DataFrame = None, table_fields: dict = None
) -> None:
    # Insert data from dataframe to database
    if table_name is None or dataset is None or table_fields is None:
        raise ValueError("table_name, dataset and table_fields must be provided")

    # Prepare SQL statement
    logger.info(f"Creating TABLE '{table_name}'")

    sql_statement = f"""
     CREATE TABLE IF NOT EXISTS {table_name} ( 
     id SERIAL """

    for key, value in table_fields.items():
        sql_statement += f", {key} {value['type']}"
        if value["type"] == "VARCHAR":
            sql_statement += f"({value['length']})"
    sql_statement += ");"

    logger.info(f"Creating INDEXES for table '{table_name}'")

    for key, value in table_fields.items():
        if {value["index"]}:
            sql_statement += f" CREATE INDEX IF NOT EXISTS idx_{table_name}_{key} on {table_name}({key}); \n "

    logger.info(f"sql_statement: {sql_statement}")
    logger.info("Acquiring DB CONN at insert_data()")

    cursor: psycopg2.extensions.cursor = process_db_data(sql_statement)

    if cursor.rowcount == -1:
        result = f"Table {table_name} successfully created."
    elif cursor.rowcount == 0:
        result = f"Table {table_name} already exists."
    else:
        raise RuntimeError(f"Error while creating {table_name}.")

    logger.info(
        f"Inserting dataset result = {result} cursor.rowcount {cursor.rowcount}"
    )

    # Table Ok, let's insert data
    # Insert Data
    logger.info(
        f"Inserting dataset with length {len(dataset)} into '{table_name}' table"
    )
    sql_statement = f"""INSERT INTO {table_name} ("""
    for field, _ in table_fields.items():
        sql_statement += f" {field}, "

    sql_statement = sql_statement[:-2]  # Remove the last trailing comma and space
    sql_statement += f") VALUES ({'%s, ' * len(table_fields)}"
    sql_statement = sql_statement[:-2]  # Remove the last trailing comma and space
    sql_statement += ")"

    logger.info(f"sql_statement: {sql_statement}")

    # id, name, age) VALUES (%s, %s, %s) ON CONFLICT (id) DO NOTHING"""
    data_tuples = list(
        dataset.itertuples(index=False, name=None)
    )  # Convert DataFrame to list of tuples
    cursor: psycopg2.extensions.cursor = process_db_data(
        sql_command=sql_statement,
        data=data_tuples,
        executemany=True,
    )

    print(f"Lines inserted = {cursor.rowcount} Line in dataset: {len(data_tuples)}")
    # cur.executemany(insert_query, data_tuples)  # Efficient batch insert
    #
    # Commit and Close
    # conn.commit()
    # cur.close()
    # conn.close()


def main():
    logger.info(f"BASE_DIR: {BASE_DIR}")
    logger.info(f"DATA_FILE: {DATA_FILE}")

    # Get the number of lines in raw file
    # Not using "readlines()" once it loads all file in memory
    with open(DATA_FILE, encoding="ISO-8859-1") as in_file:
        for count, lines in enumerate(in_file, start=1):
            pass

    logger.info(f"Number of raw lines: {count}")

    # Using Pandas to bypass eventual malformed lines.
    # Not a very good practice.
    # We should be doing a data cleanup first
    df = pd.read_csv(
        DATA_FILE, header=0, encoding="ISO-8859-1", on_bad_lines="skip", sep=";"
    )

    logger.info(f"Number of df lines: {len(df)}")
    logger.info(f"Lines lost: {count - len(df)}")

    # Store data to DB
    insert_data_from_df_to_db(
        table_name=settings.POSTGRES_DB, dataset=df, table_fields=BOOK_TABLE_FIELDS
    )


if __name__ == "__main__":
    main()
    close_pool()
