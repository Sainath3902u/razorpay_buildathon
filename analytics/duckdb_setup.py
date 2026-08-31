import duckdb
from pathlib import Path


def create_connection():
    return duckdb.connect()


def load_dataset(connection, parquet_path):

    connection.execute(
        f"""
        CREATE OR REPLACE VIEW revenue_data AS
        SELECT *
        FROM read_parquet('{parquet_path}')
        """
    )

    return connection