{{
    config(
        materialized='incremental',
        unique_key='sales_detail_id',
        incremental_strategy='delete+insert'
    )
}}

with sales_details as (

    select * from {{ ref('stg_petstore__sales_details') }}

),

sales as (

    select * from {{ ref('stg_petstore__sales') }}

    {% if is_incremental() %}
    where order_date >= (select max(order_date) from {{ this }})
    {% endif %}

),

final as (

    select
        sales_details.sales_detail_id,
        sales_details.sales_id,
        sales.customer_id,
        sales_details.product_id,
        sales.order_date,
        sales_details.quantity,
        sales_details.unit_price,
        sales_details.amount

    from sales_details
    inner join sales
        on sales_details.sales_id = sales.sales_id

)

select * from final
