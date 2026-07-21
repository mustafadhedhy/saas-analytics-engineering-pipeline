with events as (

    select *
    from {{ ref('stg_events') }}

),

final as (

    select
        event_id,
        user_id,
        account_id,
        event_type,
        event_timestamp,
        event_timestamp::date as event_date,
        date_trunc('month', event_timestamp)::date as event_month,
        session_id
    from events

)

select *
from final