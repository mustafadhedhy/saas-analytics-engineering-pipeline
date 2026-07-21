# Project Walkthrough

## Project Overview

This project is an end-to-end analytics engineering pipeline for a synthetic SaaS business.

The goal of the project is to transform raw product, customer, subscription, and support data into clean, tested, dashboard-ready analytics tables. The final output is a Power BI Executive Summary dashboard that helps business users understand customer activity, recurring revenue, product usage, support performance, and account health.

This project simulates a real analytics workflow where data is generated, loaded into a database, transformed using dbt, validated with tests, and visualized in Power BI.

## Tools and Technologies Used

The project uses the following tools and technologies:

- Python
- PostgreSQL
- SQL
- dbt
- Power BI
- Git / GitHub
- Pandas
- NumPy
- Faker
- SQLAlchemy
- python-dotenv

## Final Data Flow

```text
Python synthetic data generation
        ↓
CSV source files
        ↓
PostgreSQL raw schema
        ↓
dbt staging views
        ↓
dbt mart tables
        ↓
Power BI Executive Summary dashboard
```

## Step 1: Project Setup

The project started with a clean folder structure, a Python virtual environment, a Git repository, and a PostgreSQL database.

The PostgreSQL database is named:

```text
saas_analytics
```

Three schemas were created inside PostgreSQL:

```text
raw
staging
marts
```

Each schema has a specific role in the analytics workflow.

| Schema | Purpose |
|---|---|
| raw | Stores source-like data loaded from CSV files |
| staging | Stores cleaned and standardized dbt views |
| marts | Stores business-ready tables used for reporting and Power BI |

This layered structure makes the pipeline easier to understand, test, debug, and maintain.

## Step 2: Synthetic SaaS Data Generation

Synthetic SaaS data was generated using Python, Pandas, NumPy, and Faker.

The generated data represents a SaaS business with customer accounts, users, subscriptions, product usage events, and support tickets.

Generated datasets:

| Dataset | Rows | Description |
|---|---:|---|
| Accounts | 500 | Customer account information |
| Users | 5,000 | Users linked to customer accounts |
| Subscriptions | 650 | Subscription and revenue records |
| Product events | 200,000 | Product usage event data |
| Support tickets | 8,000 | Customer support ticket records |

Total records generated:

```text
214,150+
```

The data generation script creates realistic SaaS activity such as:

- Customer accounts across different countries and industries
- Users with different roles
- Active and inactive users
- Subscription plans such as Free, Starter, Professional, and Enterprise
- Product usage events such as login, dashboard views, AI feature usage, report exports, and file uploads
- Support tickets with priority, status, category, created date, and resolved date

The data generation script is located at:

```text
data_generation/generate_saas_data.py
```

## Step 3: Data Inspection

After generating the CSV files, a data inspection script was created to validate the generated datasets.

The inspection script checks:

- Row counts
- Column names
- Missing values
- Sample records

The inspection script is located at:

```text
scripts/inspect_generated_data.py
```

This step helped confirm that the generated source files were complete and ready to load into PostgreSQL.

## Step 4: Raw Data Loading into PostgreSQL

The generated CSV files were loaded into PostgreSQL under the `raw` schema.

Raw tables created:

```text
raw.raw_accounts
raw.raw_users
raw.raw_subscriptions
raw.raw_events
raw.raw_support_tickets
```

The ingestion script is located at:

```text
ingestion/load_raw_data_to_postgres.py
```

The script connects to PostgreSQL using environment variables stored in a local `.env` file.

The `.env` file is excluded from GitHub using `.gitignore` to avoid exposing database credentials.

A validation script was also created to confirm that all expected row counts were loaded successfully into PostgreSQL.

The validation script is located at:

```text
scripts/validate_raw_tables.py
```

Expected raw table row counts:

| Raw Table | Expected Rows |
|---|---:|
| raw.raw_accounts | 500 |
| raw.raw_users | 5,000 |
| raw.raw_subscriptions | 650 |
| raw.raw_events | 200,000 |
| raw.raw_support_tickets | 8,000 |

## Step 5: dbt Setup

dbt was configured to connect to the PostgreSQL database.

The dbt project is located in:

```text
dbt_saas_analytics/
```

The dbt project configuration is stored in:

```text
dbt_saas_analytics/dbt_project.yml
```

The dbt profile connects to:

```text
Database: saas_analytics
Schema: staging
Adapter: postgres
```

A custom schema macro was added so that dbt creates models in the correct PostgreSQL schemas:

```text
staging
marts
```

This prevents dbt from creating unwanted schema names such as `staging_staging`.

## Step 6: dbt Staging Models

dbt staging models were created from the raw tables.

Staging models:

```text
staging.stg_accounts
staging.stg_users
staging.stg_subscriptions
staging.stg_events
staging.stg_support_tickets
```

The staging layer performs light cleaning and standardization.

Main staging tasks include:

- Selecting required fields
- Renaming columns where needed
- Casting date and timestamp columns
- Casting numeric and boolean fields
- Preparing source data for downstream mart models

The staging models are materialized as views because they mainly clean and standardize raw data.

## Step 7: dbt Tests for Staging Layer

dbt tests were added to validate the staging layer.

The staging layer includes tests for:

- Unique primary identifiers
- Not-null important fields
- Relationships between accounts, users, subscriptions, events, and support tickets

Examples of tested fields:

| Model | Tested Fields |
|---|---|
| stg_accounts | account_id |
| stg_users | user_id, account_id |
| stg_subscriptions | subscription_id, account_id |
| stg_events | event_id, user_id, account_id |
| stg_support_tickets | ticket_id, account_id |

The staging layer successfully passed:

```text
25 dbt data tests
```

This confirms that the cleaned staging views are reliable for downstream transformations.

## Step 8: dbt Mart Models

The mart layer creates analytics-ready tables for business reporting and Power BI.

Mart models created:

```text
marts.dim_accounts
marts.fct_events
marts.fct_subscriptions
marts.fct_support_tickets
marts.mart_account_health
marts.mart_monthly_product_usage
marts.mart_plan_revenue_summary
```

The mart layer is materialized as tables because these models are used directly for reporting and dashboard performance.

## Step 9: Dimension and Fact Tables

The project uses a simple dimensional model.

The main dimension table is:

```text
marts.dim_accounts
```

This table contains account-level descriptive information such as:

- Account ID
- Account name
- Industry
- Country
- Plan type
- Created date
- Total users
- Active users

The main fact tables are:

```text
marts.fct_events
marts.fct_subscriptions
marts.fct_support_tickets
```

These fact tables store measurable business activities.

### fct_events

This table stores product usage events.

It supports analysis of:

- Total product events
- Event types
- Active users
- Active accounts
- Sessions
- Monthly usage trends
- AI feature usage
- Dashboard usage
- Export activity

### fct_subscriptions

This table stores subscription and revenue information.

It includes the calculated field:

```text
active_mrr
```

The logic is:

```text
If subscription_status = active, active_mrr = monthly_revenue
Otherwise, active_mrr = 0
```

This allows the dashboard to track active monthly recurring revenue.

### fct_support_tickets

This table stores customer support ticket information.

It includes the calculated field:

```text
resolution_hours
```

This measures how long it took to resolve each support ticket.

## Step 10: Account Health Mart

The main business mart is:

```text
marts.mart_account_health
```

This model combines account, user, product usage, subscription, and support data into one account-level table.

It includes:

- Account attributes
- User counts
- Product usage metrics
- Recent activity metrics
- Revenue metrics
- Support ticket metrics
- Account health classification

Important fields include:

| Field | Description |
|---|---|
| account_id | Unique account identifier |
| account_name | Customer account name |
| industry | Customer industry |
| country | Customer country |
| plan_type | Subscription plan type |
| total_users | Total users linked to the account |
| active_users | Active users linked to the account |
| total_events | Total product usage events for the account |
| active_event_users | Users who generated product events |
| total_sessions | Total sessions for the account |
| last_event_at | Most recent product event timestamp |
| events_last_30_days | Recent usage activity |
| active_mrr | Active monthly recurring revenue |
| total_tickets | Total support tickets |
| open_tickets | Open or in-progress support tickets |
| avg_resolution_hours | Average support resolution time |
| account_health_status | Health classification of the account |

## Step 11: Account Health Logic

Account health is calculated using product usage, active revenue, and support activity.

Accounts are classified into three categories:

| Status | Meaning |
|---|---|
| Healthy | Strong recent usage, active revenue, and low open support burden |
| Monitor | Moderate usage or active revenue |
| At Risk | Low recent activity and weaker engagement indicators |

The account health logic uses:

- Product events in the latest 30-day period
- Active monthly recurring revenue
- Number of open support tickets

This helps customer success and leadership teams identify which accounts may need attention.

## Step 12: Dashboard-Ready Marts

Two additional mart tables were created specifically for dashboarding.

### mart_monthly_product_usage

This table summarizes product usage by month.

It supports visuals such as:

- Total events over time
- Active users over time
- Active accounts over time
- Total sessions over time
- AI feature usage trend
- Dashboard usage trend
- Export activity trend

### mart_plan_revenue_summary

This table summarizes revenue, usage, support, and account health by plan type.

It supports visuals such as:

- Active MRR by plan type
- Accounts by plan type
- Healthy accounts by plan type
- At-risk accounts by plan type
- Product usage by plan type
- Support tickets by plan type

These tables make Power BI dashboard building easier and faster.

## Step 13: Business KPI Validation

A Python KPI validation script was created to check key business metrics directly from PostgreSQL.

The script validates:

- Total accounts
- Total users
- Active users
- Total product events
- Active monthly recurring revenue
- Support ticket volume
- Account health distribution
- Revenue by plan type
- Product events by type
- Support performance by priority

The KPI validation script is located at:

```text
scripts/validate_business_kpis.py
```

This script helps verify that the mart tables produce meaningful business metrics before connecting them to Power BI.

## Step 14: Power BI Dashboard

Power BI connects to the `marts` schema only.

The dashboard does not use raw or staging tables directly. This keeps the reporting layer clean and business-friendly.

The current dashboard includes one page:

```text
Executive Summary
```

The Executive Summary page includes:

- Total accounts
- Total users
- Active users
- Active MRR
- Total product events
- Open support tickets
- Account health distribution
- Active MRR by plan type
- Accounts by country
- At-risk account detail table
- Plan type slicer
- Country slicer

The dashboard allows business users to quickly understand the current state of customer activity, revenue, and account health.

## Business Questions Answered

This project can help answer questions such as:

- How many customer accounts does the SaaS business have?
- How many total and active users are there?
- How much active monthly recurring revenue is being generated?
- Which plan types generate the most revenue?
- Which accounts are healthy, monitored, or at risk?
- Which countries have the largest customer base?
- How many product events were generated?
- Which accounts have open support issues?
- Which customer accounts may need attention from customer success teams?

## Business Value

This project demonstrates how raw operational data can be transformed into business-ready analytics.

The final analytics layer supports:

- Customer success monitoring
- Product usage analysis
- Revenue tracking
- Support performance analysis
- Executive reporting
- Business intelligence dashboarding

The project shows a complete workflow from source data to final dashboard.

## Skills Demonstrated

This project demonstrates the following technical and analytical skills:

- Python-based synthetic data generation
- Data ingestion into PostgreSQL
- SQL-based data transformation
- dbt project setup and configuration
- dbt staging and mart modeling
- Data quality testing with dbt
- KPI validation using Python and SQLAlchemy
- Dimensional modeling concepts
- Business KPI design
- Power BI dashboard development
- Git and GitHub version control
- Analytics engineering workflow design
- Documentation and project communication

## Challenges Solved

During the project, several practical issues were handled:

- PostgreSQL setup and connection testing
- Python virtual environment package management
- Loading large event data into PostgreSQL
- dbt profile configuration
- dbt schema naming configuration
- Relationship testing between data models
- Account health logic refinement
- Power BI model relationship cleanup
- GitHub push and rebase workflow

These are realistic tasks that often appear in real analytics and data engineering projects.

## Final Outcome

The final project includes:

- Synthetic SaaS source data generation
- PostgreSQL raw data ingestion
- dbt staging models
- dbt mart models
- dbt data tests
- Business KPI validation script
- Power BI Executive Summary dashboard
- Business insights documentation
- Data model documentation
- GitHub portfolio repository

## Interview Summary

This project is a portfolio-ready analytics engineering pipeline.

It simulates how a SaaS company can transform operational product, customer, subscription, and support data into tested analytics models and a Power BI dashboard.

The project demonstrates the full workflow from data generation to data modeling, KPI validation, and final business reporting.

A strong interview explanation would be:

> I built an end-to-end analytics engineering pipeline for a synthetic SaaS business using Python, PostgreSQL, dbt, SQL, and Power BI. I generated realistic source data for accounts, users, subscriptions, product events, and support tickets, loaded it into PostgreSQL, created dbt staging and mart models, added data quality tests, validated business KPIs, and built a Power BI Executive Summary dashboard to track account health, active MRR, product usage, and support performance.
