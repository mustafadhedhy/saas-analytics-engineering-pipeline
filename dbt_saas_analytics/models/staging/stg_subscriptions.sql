with source as (

    select *
    from {{ source('raw', 'raw_subscriptions') }}

),

renamed as (

    select
        subscription_id,
        account_id,
        plan_type,
        monthly_revenue::numeric as monthly_revenue,
        start_date::date as start_date,
        end_date::date as end_date,
        status as subscription_status
    from source

)

select *
from renamed