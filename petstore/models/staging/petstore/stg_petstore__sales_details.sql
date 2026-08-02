with source as (

    select * from {{ source('petstore', 'sales_detail') }}

),

renamed as (

    select
        sales_detail_id,
        sales_id,
        product_id,
        quantity,
        unit_price,
        amount

    from source

)

select * from renamed
