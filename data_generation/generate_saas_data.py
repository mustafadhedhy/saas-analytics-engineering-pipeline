import random
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
from faker import Faker


# -----------------------------
# Configuration
# -----------------------------

SEED = 42

N_ACCOUNTS = 500
N_USERS = 5000
N_EVENTS = 200000
N_SUBSCRIPTIONS = 650
N_TICKETS = 8000

OUTPUT_DIR = Path("data")

fake = Faker()
Faker.seed(SEED)
random.seed(SEED)
np.random.seed(SEED)


# -----------------------------
# Helper functions
# -----------------------------

def random_dates(start_date: str, end_date: str, n: int) -> pd.Series:
    """Generate n random timestamps between start_date and end_date."""
    start_ts = int(pd.Timestamp(start_date).timestamp())
    end_ts = int(pd.Timestamp(end_date).timestamp())
    random_ts = np.random.randint(start_ts, end_ts, n)
    return pd.Series(pd.to_datetime(random_ts, unit="s"))


def weighted_choice(options: list[str], probabilities: list[float], n: int) -> np.ndarray:
    """Generate weighted random choices."""
    return np.random.choice(options, size=n, p=probabilities)


# -----------------------------
# Generate accounts
# -----------------------------

def generate_accounts() -> pd.DataFrame:
    industries = [
        "SaaS",
        "FinTech",
        "Healthcare",
        "Education",
        "Retail",
        "Manufacturing",
        "Consulting",
        "Marketing",
    ]

    countries = [
        "Belgium",
        "Netherlands",
        "Germany",
        "Denmark",
        "Sweden",
        "Finland",
        "France",
        "Ireland",
        "Estonia",
        "Luxembourg",
    ]

    plan_types = ["Free", "Starter", "Professional", "Enterprise"]
    plan_probs = [0.20, 0.35, 0.30, 0.15]

    accounts = []

    for i in range(1, N_ACCOUNTS + 1):
        account_id = f"ACC-{i:04d}"

        accounts.append(
            {
                "account_id": account_id,
                "account_name": fake.company(),
                "industry": random.choice(industries),
                "country": random.choice(countries),
                "plan_type": np.random.choice(plan_types, p=plan_probs),
                "created_at": random_dates("2024-01-01", "2026-06-30", 1).iloc[0],
            }
        )

    return pd.DataFrame(accounts)


# -----------------------------
# Generate users
# -----------------------------

def generate_users(accounts_df: pd.DataFrame) -> pd.DataFrame:
    user_roles = ["Admin", "Manager", "Analyst", "Support", "Viewer"]
    role_probs = [0.12, 0.18, 0.25, 0.20, 0.25]

    account_ids = accounts_df["account_id"].tolist()

    users = []

    for i in range(1, N_USERS + 1):
        account_id = random.choice(account_ids)
        account_created_at = accounts_df.loc[
            accounts_df["account_id"] == account_id, "created_at"
        ].iloc[0]

        signup_start = max(pd.Timestamp(account_created_at), pd.Timestamp("2024-01-01"))
        signup_date = random_dates(
            signup_start.strftime("%Y-%m-%d"), "2026-07-01", 1
        ).iloc[0]

        users.append(
            {
                "user_id": f"USR-{i:06d}",
                "account_id": account_id,
                "user_role": np.random.choice(user_roles, p=role_probs),
                "signup_date": signup_date,
                "is_active": np.random.choice([True, False], p=[0.82, 0.18]),
            }
        )

    return pd.DataFrame(users)


# -----------------------------
# Generate subscriptions
# -----------------------------

def generate_subscriptions(accounts_df: pd.DataFrame) -> pd.DataFrame:
    plan_revenue = {
        "Free": 0,
        "Starter": 99,
        "Professional": 299,
        "Enterprise": 999,
    }

    subscription_statuses = ["active", "cancelled", "trial", "past_due"]
    status_probs = [0.72, 0.12, 0.10, 0.06]

    subscriptions = []

    account_ids = accounts_df["account_id"].tolist()

    for i in range(1, N_SUBSCRIPTIONS + 1):
        account_id = random.choice(account_ids)
        account_plan = accounts_df.loc[
            accounts_df["account_id"] == account_id, "plan_type"
        ].iloc[0]

        status = np.random.choice(subscription_statuses, p=status_probs)
        start_date = random_dates("2024-01-01", "2026-06-30", 1).iloc[0]

        monthly_revenue = plan_revenue[account_plan]

        # Add realistic variation to paid plans
        if monthly_revenue > 0:
            monthly_revenue = int(monthly_revenue * np.random.uniform(0.85, 1.25))

        if status == "cancelled":
            end_date = start_date + timedelta(days=int(np.random.randint(30, 500)))
            if end_date > pd.Timestamp("2026-07-01"):
                end_date = pd.NaT
                status = "active"
        else:
            end_date = pd.NaT

        subscriptions.append(
            {
                "subscription_id": f"SUB-{i:06d}",
                "account_id": account_id,
                "plan_type": account_plan,
                "monthly_revenue": monthly_revenue,
                "start_date": start_date.date(),
                "end_date": end_date.date() if pd.notnull(end_date) else None,
                "status": status,
            }
        )

    return pd.DataFrame(subscriptions)


# -----------------------------
# Generate product events
# -----------------------------

def generate_events(accounts_df: pd.DataFrame, users_df: pd.DataFrame) -> pd.DataFrame:
    event_types = [
        "login",
        "create_project",
        "invite_user",
        "upload_file",
        "use_ai_feature",
        "export_report",
        "create_dashboard",
        "view_dashboard",
        "billing_page_view",
        "support_page_view",
    ]

    event_probs = [
        0.30,  # login
        0.10,  # create_project
        0.06,  # invite_user
        0.12,  # upload_file
        0.09,  # use_ai_feature
        0.08,  # export_report
        0.05,  # create_dashboard
        0.13,  # view_dashboard
        0.03,  # billing_page_view
        0.04,  # support_page_view
    ]

    sampled_users = users_df.sample(
        n=N_EVENTS,
        replace=True,
        weights=users_df["is_active"].map({True: 0.9, False: 0.1}),
        random_state=SEED,
    ).reset_index(drop=True)

    events_df = pd.DataFrame(
        {
            "event_id": [f"EVT-{i:08d}" for i in range(1, N_EVENTS + 1)],
            "user_id": sampled_users["user_id"],
            "account_id": sampled_users["account_id"],
            "event_type": weighted_choice(event_types, event_probs, N_EVENTS),
            "event_timestamp": random_dates("2025-01-01", "2026-07-01", N_EVENTS),
            "session_id": [
                f"SES-{np.random.randint(1, 60000):07d}" for _ in range(N_EVENTS)
            ],
        }
    )

    return events_df


# -----------------------------
# Generate support tickets
# -----------------------------

def generate_support_tickets(accounts_df: pd.DataFrame) -> pd.DataFrame:
    priorities = ["low", "medium", "high", "urgent"]
    priority_probs = [0.45, 0.35, 0.15, 0.05]

    statuses = ["open", "in_progress", "resolved", "closed"]
    status_probs = [0.12, 0.18, 0.45, 0.25]

    categories = [
        "billing",
        "technical_issue",
        "login_access",
        "feature_request",
        "data_export",
        "integration",
        "ai_assistant",
        "performance",
    ]

    account_ids = accounts_df["account_id"].tolist()

    created_dates = random_dates("2025-01-01", "2026-07-01", N_TICKETS)

    tickets = []

    for i in range(1, N_TICKETS + 1):
        created_at = created_dates.iloc[i - 1]
        status = np.random.choice(statuses, p=status_probs)

        if status in ["resolved", "closed"]:
            resolution_hours = int(np.random.randint(2, 240))
            resolved_at = created_at + timedelta(hours=resolution_hours)
        else:
            resolved_at = None

        tickets.append(
            {
                "ticket_id": f"TCK-{i:07d}",
                "account_id": random.choice(account_ids),
                "created_at": created_at,
                "resolved_at": resolved_at,
                "priority": np.random.choice(priorities, p=priority_probs),
                "status": status,
                "category": random.choice(categories),
            }
        )

    return pd.DataFrame(tickets)


# -----------------------------
# Main
# -----------------------------

def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Generating accounts...")
    accounts_df = generate_accounts()

    print("Generating users...")
    users_df = generate_users(accounts_df)

    print("Generating subscriptions...")
    subscriptions_df = generate_subscriptions(accounts_df)

    print("Generating product events...")
    events_df = generate_events(accounts_df, users_df)

    print("Generating support tickets...")
    support_tickets_df = generate_support_tickets(accounts_df)

    accounts_df.to_csv(OUTPUT_DIR / "raw_accounts.csv", index=False)
    users_df.to_csv(OUTPUT_DIR / "raw_users.csv", index=False)
    subscriptions_df.to_csv(OUTPUT_DIR / "raw_subscriptions.csv", index=False)
    events_df.to_csv(OUTPUT_DIR / "raw_events.csv", index=False)
    support_tickets_df.to_csv(OUTPUT_DIR / "raw_support_tickets.csv", index=False)

    print("\nSynthetic SaaS data generated successfully.")
    print(f"Accounts: {len(accounts_df):,}")
    print(f"Users: {len(users_df):,}")
    print(f"Subscriptions: {len(subscriptions_df):,}")
    print(f"Events: {len(events_df):,}")
    print(f"Support tickets: {len(support_tickets_df):,}")
    print(f"\nFiles saved in: {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    main()