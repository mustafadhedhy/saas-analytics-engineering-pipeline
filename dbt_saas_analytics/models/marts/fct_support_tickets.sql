with tickets as (

    select *
    from {{ ref('stg_support_tickets') }}

),

final as (

    select
        ticket_id,
        account_id,
        created_at,
        resolved_at,
        created_at::date as created_date,
        date_trunc('month', created_at)::date as created_month,
        priority,
        ticket_status,
        category,
        case
            when resolved_at is not null
            then extract(epoch from (resolved_at - created_at)) / 3600
            else null
        end as resolution_hours
    from tickets

)

select *
from final