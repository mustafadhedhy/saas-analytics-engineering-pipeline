with accounts as (

    select *
    from {{ ref('stg_accounts') }}

),

users_aggregated as (

    select
        account_id,
        count(*) as total_users,
        count(*) filter (where is_active = true) as active_users
    from {{ ref('stg_users') }}
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
        coalesce(u.total_users, 0) as total_users,
        coalesce(u.active_users, 0) as active_users
    from accounts a
    left join users_aggregated u
        on a.account_id = u.account_id

)

select *
from final