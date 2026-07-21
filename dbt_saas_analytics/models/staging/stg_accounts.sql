with source as (

    select *
    from {{ source('raw', 'raw_accounts') }}

),

renamed as (

    select
        account_id,
        account_name,
        industry,
        country,
        plan_type,
        created_at::timestamp as created_at
    from source

)

select *
from renamed