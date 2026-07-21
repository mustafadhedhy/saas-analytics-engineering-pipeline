with account_health as (

    select *
    from {{ ref('mart_account_health') }}

),

plan_summary as (

    select
        plan_type,
        count(*) as total_accounts,
        count(*) filter (where account_health_status = 'Healthy') as healthy_accounts,
        count(*) filter (where account_health_status = 'Monitor') as monitor_accounts,
        count(*) filter (where account_health_status = 'At Risk') as at_risk_accounts,

        sum(total_users) as total_users,
        sum(active_users) as active_users,
        sum(total_events) as total_events,
        sum(events_last_30_days) as events_last_30_days,

        sum(active_mrr) as total_active_mrr,
        round(avg(active_mrr), 2) as avg_active_mrr_per_account,

        sum(total_tickets) as total_support_tickets,
        sum(open_tickets) as total_open_tickets,
        round(avg(avg_resolution_hours), 2) as avg_resolution_hours

    from account_health
    group by plan_type

)

select *
from plan_summary
order by total_active_mrr desc