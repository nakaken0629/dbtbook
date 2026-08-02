with customers as (

    select * from {{ ref('stg_petstore__customers') }}

),

final as (

    select
        customer_id,
        customer_name,
        email,
        address,
        registered_at

    from customers

)

select * from final
