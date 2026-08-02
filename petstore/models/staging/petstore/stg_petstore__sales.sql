with source as (

    select * from {{ source('petstore', 'sales') }}

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
