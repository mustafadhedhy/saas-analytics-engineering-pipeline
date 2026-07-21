with events as (

    select *
    from {{ ref('fct_events') }}

),

monthly_usage as (

    select
        event_month,
        count(*) as total_events,
        count(distinct account_id) as active_accounts,
        count(distinct user_id) as active_users,
        count(distinct session_id) as total_sessions,

        count(*) filter (where event_type = 'login') as login_events,
        count(*) filter (where event_type = 'view_dashboard') as dashboard_view_events,
        count(*) filter (where event_type = 'create_dashboard') as dashboard_creation_events,
        count(*) filter (where event_type = 'use_ai_feature') as ai_feature_events,
        count(*) filter (where event_type = 'export_report') as export_report_events,
        count(*) filter (where event_type = 'upload_file') as upload_file_events,
        count(*) filter (where event_type = 'create_project') as create_project_events,
        count(*) filter (where event_type = 'invite_user') as invite_user_events,
        count(*) filter (where event_type = 'billing_page_view') as billing_page_view_events,
        count(*) filter (where event_type = 'support_page_view') as support_page_view_events

    from events
    group by event_month

)

select *
from monthly_usage
order by event_month