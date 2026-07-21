with subscriptions as (

    select *
    from {{ ref('stg_subscriptions') }}

),

final as (

    select
        subscription_id,
        account_id,
        plan_type,
        monthly_revenue,
        start_date,
        end_date,
        subscription_status,
        case
            when subscription_status = 'active' then monthly_revenue
            else 0
        end as active_mrr
    from subscriptions

)

select *
from final