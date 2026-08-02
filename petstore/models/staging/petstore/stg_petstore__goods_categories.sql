with source as (

    select * from {{ source('petstore', 'goods_category_master') }}

),

renamed as (

    select
        goods_category_id,
        goods_category_name

    from source

)

select * from renamed
