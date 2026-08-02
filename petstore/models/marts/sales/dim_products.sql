with products as (

    select * from {{ ref('stg_petstore__products') }}

),

species as (

    select * from {{ ref('stg_petstore__species') }}

),

goods_categories as (

    select * from {{ ref('stg_petstore__goods_categories') }}

),

final as (

    select
        products.product_id,
        products.product_type,
        products.product_name,
        products.price,
        products.is_active,
        products.species_id,
        species.species_name,
        products.goods_category_id,
        goods_categories.goods_category_name,
        products.description

    from products
    left join species
        on products.species_id = species.species_id
    left join goods_categories
        on products.goods_category_id = goods_categories.goods_category_id

)

select * from final
