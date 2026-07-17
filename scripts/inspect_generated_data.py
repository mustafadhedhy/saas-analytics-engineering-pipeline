from pathlib import Path
import pandas as pd


DATA_DIR = Path("data")

FILES = [
    "raw_accounts.csv",
    "raw_users.csv",
    "raw_subscriptions.csv",
    "raw_events.csv",
    "raw_support_tickets.csv",
]


def main() -> None:
    print("Synthetic data inspection\n")

    for file_name in FILES:
        file_path = DATA_DIR / file_name

        if not file_path.exists():
            print(f"{file_name}: missing")
            continue

        df = pd.read_csv(file_path)

        print("=" * 80)
        print(file_name)
        print(f"Rows: {len(df):,}")
        print(f"Columns: {len(df.columns)}")

        print("\nColumn names:")
        print(list(df.columns))

        print("\nMissing values:")
        print(df.isna().sum())

        print("\nSample rows:")
        print(df.head(3))
        print()


if __name__ == "__main__":
    main()