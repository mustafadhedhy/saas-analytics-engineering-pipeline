import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text


def get_database_engine():
    load_dotenv()

    connection_url = (
        f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )

    return create_engine(connection_url)


def run_query(connection, title, query):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)

    results = connection.execute(text(query)).fetchall()

    for row in results:
        print(dict(row._mapping))


def main():
    engine = get_database_engine()

    with engine.connect() as connection:
        run_query(
            connection,
            "Overall SaaS KPIs",
            """
            select
                count(*) as total_accounts,
                sum(total_users) as total_users,
                sum(active_users) as active_users,
                sum(total_events) as total_events,
                sum(active_mrr) as total_active_mrr,
                sum(total_tickets) as total_support_tickets
            from marts.mart_account_health;
            """,
        )

        run_query(
            connection,
            "Account Health Distribution",
            """
            select
                account_health_status,
                count(*) as account_count
            from marts.mart_account_health
            group by account_health_status
            order by account_count desc;
            """,
        )

        run_query(
            connection,
            "Revenue by Plan Type",
            """
            select
                plan_type,
                count(*) as account_count,
                sum(active_mrr) as total_active_mrr,
                round(avg(active_mrr), 2) as avg_active_mrr
            from marts.mart_account_health
            group by plan_type
            order by total_active_mrr desc;
            """,
        )

        run_query(
            connection,
            "Top Product Events",
            """
            select
                event_type,
                count(*) as total_events
            from marts.fct_events
            group by event_type
            order by total_events desc
            limit 10;
            """,
        )

        run_query(
            connection,
            "Support Performance by Priority",
            """
            select
                priority,
                count(*) as total_tickets,
                count(*) filter (where ticket_status in ('open', 'in_progress')) as open_tickets,
                round(avg(resolution_hours), 2) as avg_resolution_hours
            from marts.fct_support_tickets
            group by priority
            order by total_tickets desc;
            """,
        )


if __name__ == "__main__":
    main()