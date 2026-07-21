# Data Model Summary

This project follows a layered analytics engineering design to transform raw SaaS operational data into clean, tested, and dashboard-ready analytics tables.

The data model is designed around four main layers:

1. Raw layer
2. Staging layer
3. Mart layer
4. Power BI dashboard layer

## Data Flow

```text
Synthetic SaaS CSV Files
        ↓
PostgreSQL Raw Schema
        ↓
dbt Staging Views
        ↓
dbt Mart Tables
        ↓
Power BI Dashboard
```

## Project Database

The PostgreSQL database used in this project is:

```text
saas_analytics
```

The database contains three main schemas:

```text
raw
staging
marts
```

Each schema has a different purpose in the analytics workflow.

## Raw Layer

The raw layer stores source-like data loaded from generated CSV files into PostgreSQL.

Schema:

```text
raw
```

Raw tables:

| Table | Description |
|---|---|
| raw.raw_accounts | Customer account information including company, country, industry, plan type, and creation date |
| raw.raw_users | Users linked to customer accounts, including role and active status |
| raw.raw_subscriptions | Subscription records including plan type, monthly revenue, start date, end date, and status |
| raw.raw_events | Product usage events such as login, dashboard views, AI feature usage, report exports, and file uploads |
| raw.raw_support_tickets | Customer support tickets including priority, status, category, created date, and resolved date |

The raw layer is kept close to the original source structure. Minimal transformation is applied at this stage. Its main purpose is to store the ingested source data before cleaning and business transformation.

## Staging Layer

The staging layer is built using dbt views.

Schema:

```text
staging
```

Staging models:

| Model | Source Table | Purpose |
|---|---|---|
| staging.stg_accounts | raw.raw_accounts | Cleans and standardizes account-level customer data |
| staging.stg_users | raw.raw_users | Cleans user-level data and keeps the account relationship |
| staging.stg_subscriptions | raw.raw_subscriptions | Cleans subscription and recurring revenue data |
| staging.stg_events | raw.raw_events | Cleans product usage event data |
| staging.stg_support_tickets | raw.raw_support_tickets | Cleans support ticket data and prepares resolution time analysis |

The staging layer performs light transformations such as:

- Selecting required columns
- Casting date and timestamp fields
- Standardizing column names
- Preparing raw data for downstream mart models
- Keeping one staging model per raw source table

The staging layer is materialized as views because it is mainly used for cleaning and standardization.

## Mart Layer

The mart layer contains analytics-ready tables used for business analysis and Power BI dashboarding.

Schema:

```text
marts
```

Mart models:

| Model | Type | Description |
|---|---|---|
| marts.dim_accounts | Dimension table | Account dimension enriched with total users and active users |
| marts.fct_events | Fact table | Product usage event fact table with event date and event month |
| marts.fct_subscriptions | Fact table | Subscription fact table with active monthly recurring revenue calculation |
| marts.fct_support_tickets | Fact table | Support ticket fact table with resolution hours calculation |
| marts.mart_account_health | Business mart | Account-level health, usage, revenue, and support summary |
| marts.mart_monthly_product_usage | Dashboard mart | Monthly product usage summary for trend analysis |
| marts.mart_plan_revenue_summary | Dashboard mart | Plan-level revenue, usage, support, and account health summary |

The mart layer is materialized as tables because these models are used directly for reporting and dashboard performance.

## Main Entity: Account

The central business entity in this project is the customer account.

The main key used across the model is:

```text
account_id
```

Most business metrics are analyzed at the account level, including:

- Number of users
- Product usage events
- Active monthly recurring revenue
- Support ticket volume
- Open support tickets
- Account health status

## Main Relationships

The main relationships in the model are:

```text
dim_accounts.account_id → fct_events.account_id
dim_accounts.account_id → fct_subscriptions.account_id
dim_accounts.account_id → fct_support_tickets.account_id
dim_accounts.account_id → mart_account_health.account_id
```

The product event data also connects users to events:

```text
stg_users.user_id → fct_events.user_id
```

In Power BI, the main relationship design uses `dim_accounts` as the central account dimension table.

Recommended Power BI relationships:

| From Table | From Column | To Table | To Column | Relationship |
|---|---|---|---|---|
| dim_accounts | account_id | fct_events | account_id | One-to-many |
| dim_accounts | account_id | fct_subscriptions | account_id | One-to-many |
| dim_accounts | account_id | fct_support_tickets | account_id | One-to-many |
| dim_accounts | account_id | mart_account_health | account_id | One-to-one or one-to-many depending on Power BI detection |

The following summary tables are designed to be used directly in dashboard visuals and do not need forced relationships:

```text
mart_monthly_product_usage
mart_plan_revenue_summary
```

## Fact and Dimension Design

### Dimension Table

The main dimension table is:

```text
marts.dim_accounts
```

It contains descriptive account attributes:

- account_id
- account_name
- industry
- country
- plan_type
- created_at
- total_users
- active_users

This table is used to filter and describe account-level metrics.

### Fact Tables

The main fact tables are:

```text
marts.fct_events
marts.fct_subscriptions
marts.fct_support_tickets
```

These tables store measurable business activities.

#### fct_events

This table stores product usage events.

Important fields:

- event_id
- user_id
- account_id
- event_type
- event_timestamp
- event_date
- event_month
- session_id

Supported product usage analysis includes:

- Total events
- Events by type
- Monthly usage trends
- Active users
- Active accounts
- Sessions
- AI feature usage
- Dashboard usage
- Export activity

#### fct_subscriptions

This table stores subscription and revenue data.

Important fields:

- subscription_id
- account_id
- plan_type
- monthly_revenue
- start_date
- end_date
- subscription_status
- active_mrr

The `active_mrr` field calculates active monthly recurring revenue:

```text
If subscription_status = active, active_mrr = monthly_revenue
Otherwise, active_mrr = 0
```

#### fct_support_tickets

This table stores support ticket data.

Important fields:

- ticket_id
- account_id
- created_at
- resolved_at
- created_date
- created_month
- priority
- ticket_status
- category
- resolution_hours

The `resolution_hours` field calculates the time between ticket creation and resolution.

## Business Mart: Account Health

The main business mart is:

```text
marts.mart_account_health
```

This table combines account, user, product usage, subscription, and support data into one account-level table.

It includes:

- Account attributes
- User counts
- Product usage metrics
- Recent activity
- Revenue metrics
- Support ticket metrics
- Account health classification

Important fields:

| Field | Description |
|---|---|
| account_id | Unique account identifier |
| account_name | Customer account name |
| industry | Customer industry |
| country | Customer country |
| plan_type | Subscription plan type |
| total_users | Total users linked to the account |
| active_users | Active users linked to the account |
| total_events | Total product events for the account |
| active_event_users | Users who generated product events |
| total_sessions | Total sessions for the account |
| last_event_at | Most recent product event timestamp |
| ai_feature_events | Number of AI feature usage events |
| export_events | Number of report export events |
| dashboard_creation_events | Number of dashboard creation events |
| events_last_30_days | Events in the latest 30-day period based on the dataset |
| active_mrr | Active monthly recurring revenue |
| latest_subscription_status | Latest subscription status |
| total_tickets | Total support tickets |
| open_tickets | Open or in-progress tickets |
| avg_resolution_hours | Average support ticket resolution time |
| account_health_status | Final account health classification |

## Account Health Logic

The `mart_account_health` model classifies accounts based on recent product usage, active revenue, and support burden.

Accounts are grouped into three categories:

| Status | Meaning |
|---|---|
| Healthy | Strong recent usage, active revenue, and low open support burden |
| Monitor | Moderate usage or active revenue |
| At Risk | Low recent activity and weaker engagement indicators |

The account health logic uses:

- Events in the latest 30-day period
- Active monthly recurring revenue
- Number of open support tickets

This helps customer success and leadership teams identify accounts that may need attention.

## Dashboard-Ready Marts

Two additional mart tables were created specifically for Power BI dashboarding.

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

Important fields:

- event_month
- total_events
- active_accounts
- active_users
- total_sessions
- login_events
- dashboard_view_events
- dashboard_creation_events
- ai_feature_events
- export_report_events
- upload_file_events
- create_project_events
- invite_user_events
- billing_page_view_events
- support_page_view_events

### mart_plan_revenue_summary

This table summarizes revenue, usage, support, and account health by plan type.

It supports visuals such as:

- Active MRR by plan type
- Accounts by plan type
- Healthy accounts by plan type
- At-risk accounts by plan type
- Product usage by plan type
- Support tickets by plan type

Important fields:

- plan_type
- total_accounts
- healthy_accounts
- monitor_accounts
- at_risk_accounts
- total_users
- active_users
- total_events
- events_last_30_days
- total_active_mrr
- avg_active_mrr_per_account
- total_support_tickets
- total_open_tickets
- avg_resolution_hours

## Important Metrics

The mart layer supports the following business metrics:

| Metric | Source Model | Description |
|---|---|---|
| Total accounts | mart_account_health | Count of customer accounts |
| Total users | mart_account_health | Total users linked to accounts |
| Active users | mart_account_health | Active users across accounts |
| Total events | mart_account_health / fct_events | Total product usage event volume |
| Active MRR | mart_account_health / fct_subscriptions | Active monthly recurring revenue |
| Open tickets | mart_account_health / fct_support_tickets | Current unresolved support tickets |
| Average resolution hours | fct_support_tickets | Average time taken to resolve support tickets |
| Account health status | mart_account_health | Customer health classification |
| Events last 30 days | mart_account_health | Recent account engagement |
| AI feature events | mart_account_health / mart_monthly_product_usage | AI feature adoption |
| Revenue by plan type | mart_plan_revenue_summary | Active MRR grouped by subscription plan |

## Data Quality Tests

dbt tests are used to validate both staging and mart layers.

Implemented tests include:

- Unique tests for primary identifiers
- Not-null tests for important fields
- Relationship tests between accounts, users, events, subscriptions, and support tickets

Examples of tested fields:

| Model | Tested Field |
|---|---|
| stg_accounts | account_id |
| stg_users | user_id, account_id |
| stg_subscriptions | subscription_id, account_id |
| stg_events | event_id, user_id, account_id |
| stg_support_tickets | ticket_id, account_id |
| dim_accounts | account_id |
| fct_events | event_id |
| fct_subscriptions | subscription_id |
| fct_support_tickets | ticket_id |
| mart_account_health | account_id, account_health_status |
| mart_monthly_product_usage | event_month |
| mart_plan_revenue_summary | plan_type |

The staging layer successfully passed 25 dbt data tests. The mart layer includes additional tests for the final analytics-ready tables.

## Power BI Dashboard Layer

Power BI connects to the mart layer only.

The dashboard should not use raw or staging tables directly. This keeps the reporting layer clean, stable, and business-friendly.

The current Power BI dashboard includes an Executive Summary page using mart-level data.

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
- At-risk account detail
- Plan type slicer
- Country slicer

## Design Benefits

This data model provides several benefits:

- Clear separation between raw, cleaned, and business-ready data
- Reusable staging models
- Tested transformation logic
- Dashboard-ready marts for Power BI
- Easier debugging and maintenance
- Strong alignment with analytics engineering best practices
- Clear business metrics for customer success, product, revenue, and support analysis

## Summary

This data model transforms operational SaaS data into a clean analytics layer that supports business reporting and decision-making.

The raw layer stores source data, the staging layer standardizes it, the mart layer creates business-ready tables, and Power BI uses the final mart tables for dashboarding.

This structure demonstrates an end-to-end analytics engineering workflow using Python, PostgreSQL, dbt, SQL, and Power BI.
