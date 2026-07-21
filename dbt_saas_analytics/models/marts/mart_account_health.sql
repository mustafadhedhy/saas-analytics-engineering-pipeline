with accounts as (

    select *
    from {{ ref('dim_accounts') }}

),

reference_date as (

    select
        max(event_timestamp)::date as latest_event_date
    from {{ ref('fct_events') }}

),

events_aggregated as (

    select
        e.account_id,
        count(*) as total_events,
        count(distinct e.user_id) as active_event_users,
        count(distinct e.session_id) as total_sessions,
        max(e.event_timestamp) as last_event_at,
        count(*) filter (where e.event_type = 'use_ai_feature') as ai_feature_events,
        count(*) filter (where e.event_type = 'export_report') as export_events,
        count(*) filter (where e.event_type = 'create_dashboard') as dashboard_creation_events,
        count(*) filter (
            where e.event_timestamp::date >= r.latest_event_date - interval '30 days'
        ) as events_last_30_days
    from {{ ref('fct_events') }} e
    cross join reference_date r
    group by e.account_id

),

subscriptions_aggregated as (

    select
        account_id,
        sum(active_mrr) as active_mrr,
        max(subscription_status) as latest_subscription_status
    from {{ ref('fct_subscriptions') }}
    group by account_id

),

tickets_aggregated as (

    select
        account_id,
        count(*) as total_tickets,
        count(*) filter (where ticket_status in ('open', 'in_progress')) as open_tickets,
        avg(resolution_hours) as avg_resolution_hours
    from {{ ref('fct_support_tickets') }}
    group by account_id

),

final as (

    select
        a.account_id,
        a.account_name,
        a.industry,
        a.country,
        a.plan_type,
        a.created_at,
        a.total_users,
        a.active_users,

        coalesce(e.total_events, 0) as total_events,
        coalesce(e.active_event_users, 0) as active_event_users,
        coalesce(e.total_sessions, 0) as total_sessions,
        e.last_event_at,
        coalesce(e.ai_feature_events, 0) as ai_feature_events,
        coalesce(e.export_events, 0) as export_events,
        coalesce(e.dashboard_creation_events, 0) as dashboard_creation_events,
        coalesce(e.events_last_30_days, 0) as events_last_30_days,

        coalesce(s.active_mrr, 0) as active_mrr,
        s.latest_subscription_status,

        coalesce(t.total_tickets, 0) as total_tickets,
        coalesce(t.open_tickets, 0) as open_tickets,
        t.avg_resolution_hours,

        case
            when coalesce(e.events_last_30_days, 0) >= 25
                 and coalesce(t.open_tickets, 0) <= 5
                 and coalesce(s.active_mrr, 0) > 0
                then 'Healthy'

            when coalesce(e.events_last_30_days, 0) >= 8
                 or coalesce(s.active_mrr, 0) > 0
                then 'Monitor'

            else 'At Risk'
        end as account_health_status

    from accounts a
    left join events_aggregated e
        on a.account_id = e.account_id
    left join subscriptions_aggregated s
        on a.account_id = s.account_id
    left join tickets_aggregated t
        on a.account_id = t.account_id

)

select *
from final