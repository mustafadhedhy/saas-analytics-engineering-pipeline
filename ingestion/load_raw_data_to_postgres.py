import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


DATA_DIR = Path("data")

TABLES = {
    "raw_accounts.csv": "raw_accounts",
    "raw_users.csv": "raw_users",
    "raw_subscriptions.csv": "raw_subscriptions",
    "raw_events.csv": "raw_events",
    "raw_support_tickets.csv": "raw_support_tickets",
}


def get_database_engine():
    load_dotenv()

    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")

    if not all([db_host, db_port, db_name, db_user, db_password]):
        raise ValueError("Missing database credentials in .env file.")

    connection_url = (
        f"postgresql+psycopg2://{db_user}:{db_password}"
        f"@{db_host}:{db_port}/{db_name}"
    )

    return create_engine(connection_url)


def create_raw_schema(engine):
    with engine.connect() as connection:
        connection.execute(text("CREATE SCHEMA IF NOT EXISTS raw;"))
        connection.commit()


def load_csv_to_postgres(engine, csv_file: str, table_name: str):
    file_path = DATA_DIR / csv_file

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    print(f"Loading {csv_file} into raw.{table_name}...")

    df = pd.read_csv(file_path)

    df.to_sql(
        name=table_name,
        con=engine,
        schema="raw",
        if_exists="replace",
        index=False,
        chunksize=10000,
        method="multi",
    )

    print(f"Loaded {len(df):,} rows into raw.{table_name}")


def verify_loaded_tables(engine):
    query = """
    SELECT 
        schemaname,
        relname AS table_name,
        n_live_tup AS estimated_rows
    FROM pg_stat_user_tables
    WHERE schemaname = 'raw'
    ORDER BY relname;
    """

    with engine.connect() as connection:
        result = connection.execute(text(query)).fetchall()

    print("\nLoaded raw tables:")
    for row in result:
        print(f"- {row.table_name}: approximately {row.estimated_rows:,} rows")


def main():
    engine = get_database_engine()

    print("Connected to PostgreSQL successfully.")

    create_raw_schema(engine)

    for csv_file, table_name in TABLES.items():
        load_csv_to_postgres(engine, csv_file, table_name)

    verify_loaded_tables(engine)

    print("\nRaw data loading completed successfully.")


if __name__ == "__main__":
    main()