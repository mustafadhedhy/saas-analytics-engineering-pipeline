import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text


EXPECTED_TABLES = {
    "raw_accounts": 500,
    "raw_users": 5000,
    "raw_subscriptions": 650,
    "raw_events": 200000,
    "raw_support_tickets": 8000,
}


def get_database_engine():
    load_dotenv()

    connection_url = (
        f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )

    return create_engine(connection_url)


def main():
    engine = get_database_engine()

    print("Validating raw tables...\n")

    with engine.connect() as connection:
        for table_name, expected_count in EXPECTED_TABLES.items():
            query = text(f"SELECT COUNT(*) FROM raw.{table_name};")
            actual_count = connection.execute(query).scalar()

            status = "PASS" if actual_count == expected_count else "FAIL"

            print(
                f"{status} | raw.{table_name}: "
                f"expected {expected_count:,}, found {actual_count:,}"
            )

    print("\nRaw table validation completed.")


if __name__ == "__main__":
    main()