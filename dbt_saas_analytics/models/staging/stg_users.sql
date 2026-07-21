with source as (

    select *
    from {{ source('raw', 'raw_users') }}

),

renamed as (

    select
        user_id,
        account_id,
        user_role,
        signup_date::timestamp as signup_date,
        is_active::boolean as is_active
    from source

)

select *
from renamed