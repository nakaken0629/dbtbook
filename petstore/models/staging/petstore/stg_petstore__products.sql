with source as (

    select * from {{ source('petstore', 'product_master') }}

),

renamed as (

    select
        product_id,
        product_type,
        product_name,
        price,
        is_active,
        species_id,
        goods_category_id,
        description

    from source

)

select * from renamed
