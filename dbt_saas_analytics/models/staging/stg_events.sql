with source as (

    select *
    from {{ source('raw', 'raw_events') }}

),

renamed as (

    select
        event_id,
        user_id,
        account_id,
        event_type,
        event_timestamp::timestamp as event_timestamp,
        session_id
    from source

)

select *
from renamed