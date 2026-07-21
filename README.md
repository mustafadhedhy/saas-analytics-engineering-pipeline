# Modern Analytics Engineering Pipeline for SaaS Product Analytics

This project demonstrates an end-to-end analytics engineering workflow for a SaaS business. It transforms raw product, customer, subscription, and support data into structured, validated, analytics-ready datasets using Python, PostgreSQL, dbt, SQL, and Power BI.

## Business Problem

A SaaS company wants to understand product usage, customer growth, recurring revenue, churn risk, and support performance. The goal is to build a reliable analytics layer that supports self-service reporting and business decision-making for product, customer success, sales, and leadership teams.

## Project Objectives

* Generate realistic SaaS source data for accounts, users, subscriptions, product events, and support tickets
* Load raw datasets into a PostgreSQL database
* Build a structured raw data layer for future dbt transformations
* Prepare the foundation for staging models, marts, KPI definitions, data quality checks, and Power BI dashboards
* Demonstrate modern analytics engineering practices using Git, PostgreSQL, Python, SQL, and dbt

## Tech Stack

* Python
* PostgreSQL
* SQL
* dbt
* Power BI
* Git / GitHub
* Pandas
* NumPy
* Faker
* SQLAlchemy
* python-dotenv

## Planned Architecture

Synthetic SaaS Data
→ Python Data Generation
→ PostgreSQL Raw Schema
→ dbt Staging Models
→ dbt Mart Models
→ Power BI Dashboard
→ Business Insights

## Current Project Structure

```text
saas_analytics_engineering/
│
├── data/
│   ├── raw_accounts.csv
│   ├── raw_users.csv
│   ├── raw_subscriptions.csv
│   ├── raw_events.csv
│   └── raw_support_tickets.csv
│
├── data_generation/
│   └── generate_saas_data.py
│
├── ingestion/
│   └── load_raw_data_to_postgres.py
│
├── scripts/
│   ├── check_db_connection.py
│   ├── inspect_generated_data.py
│   └── validate_raw_tables.py
│
├── dbt_saas_analytics/
│
├── dashboards/
├── docs/
├── sql/
│
├── .gitignore
├── requirements.txt
└── README.md
```

## Generated Datasets

The project generates five synthetic SaaS datasets:

| Dataset                 |    Rows | Description                                                                        |
| ----------------------- | ------: | ---------------------------------------------------------------------------------- |
| raw_accounts.csv        |     500 | SaaS customer accounts with country, industry, plan type, and creation date        |
| raw_users.csv           |   5,000 | Users connected to customer accounts with roles and activity status                |
| raw_subscriptions.csv   |     650 | Subscription records with plan type, monthly revenue, start/end dates, and status  |
| raw_events.csv          | 200,000 | Product usage events such as login, dashboard views, AI feature usage, and exports |
| raw_support_tickets.csv |   8,000 | Support tickets with priority, status, category, created date, and resolved date   |

## PostgreSQL Schemas

The PostgreSQL database is named:

```text
saas_analytics
```

The following schemas have been created:

```text
raw
staging
marts
```

Current raw tables loaded into PostgreSQL:

```text
raw.raw_accounts
raw.raw_users
raw.raw_subscriptions
raw.raw_events
raw.raw_support_tickets
```

## Data Generation

Synthetic SaaS data is generated using Python, Pandas, NumPy, and Faker.

Run:

```bash
python data_generation/generate_saas_data.py
```

Expected output:

```text
Accounts: 500
Users: 5,000
Subscriptions: 650
Events: 200,000
Support tickets: 8,000
```

## Data Inspection

To inspect generated CSV files:

```bash
python scripts/inspect_generated_data.py
```

This script checks:

* Row counts
* Column names
* Missing values
* Sample rows

## Raw Data Loading

To load generated CSV files into PostgreSQL:

```bash
python ingestion/load_raw_data_to_postgres.py
```

This loads the CSV files into the PostgreSQL `raw` schema.

## Raw Table Validation

To validate raw table row counts:

```bash
python scripts/validate_raw_tables.py
```

Expected validation results:

```text
PASS | raw.raw_accounts: expected 500, found 500
PASS | raw.raw_users: expected 5,000, found 5,000
PASS | raw.raw_subscriptions: expected 650, found 650
PASS | raw.raw_events: expected 200,000, found 200,000
PASS | raw.raw_support_tickets: expected 8,000, found 8,000
```

## Environment Variables

Database credentials are stored in a local `.env` file:

```text
DB_HOST=localhost
DB_PORT=5432
DB_NAME=saas_analytics
DB_USER=postgres
DB_PASSWORD=your_postgres_password_here
```

The `.env` file is excluded from GitHub using `.gitignore`.

## Completed Progress

### Day 1: Project Setup

* Created project folder structure
* Initialized Git repository
* Created Python virtual environment
* Installed required Python packages
* Created PostgreSQL database
* Created raw, staging, and marts schemas
* Configured `.env` file
* Successfully tested PostgreSQL connection

### Day 2: Synthetic Data Generation

* Generated synthetic SaaS source data using Python
* Created datasets for accounts, users, subscriptions, product events, and support tickets
* Generated 500 accounts, 5,000 users, 650 subscriptions, 200,000 product events, and 8,000 support tickets
* Added inspection script to validate generated CSV files

### Day 3: Raw Data Loading

* Loaded generated CSV datasets into PostgreSQL
* Created raw schema tables for accounts, users, subscriptions, product events, and support tickets
* Validated row counts for all raw tables
* Confirmed raw data is ready for dbt staging models

### Day 4: dbt Setup and Staging Models

- Configured dbt project for PostgreSQL
- Created dbt profile connection to the `saas_analytics` database
- Defined raw source tables in dbt
- Created staging models for accounts, users, subscriptions, product events, and support tickets
- Materialized staging models as PostgreSQL views
- Added dbt tests for unique, not-null, and relationship checks
- Successfully ran 5 staging models
- Successfully passed 25 dbt data tests
