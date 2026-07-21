with source as (

    select *
    from {{ source('raw', 'raw_support_tickets') }}

),

renamed as (

    select
        ticket_id,
        account_id,
        created_at::timestamp as created_at,
        resolved_at::timestamp as resolved_at,
        priority,
        status as ticket_status,
        category
    from source

)

select *
from renamed