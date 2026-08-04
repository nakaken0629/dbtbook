with source as (

    select * from {{ source('petstore', 'sales') }}
    where order_date >= '{{ var("start_date", "2026-07-01") }}'
),

renamed as (

    select
        sales_id,
        customer_id,
        order_date,
        total_amount

    from source

)

select * from renamed
