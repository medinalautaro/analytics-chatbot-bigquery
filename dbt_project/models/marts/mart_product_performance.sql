{{ config(
    materialized='table',
    cluster_by=['category', 'product_id']
) }}

with product_sales as (

    select
        product_id,
        product_name,
        category,
        sum(quantity) as units_sold,
        sum(case when order_status = 'completed' then line_amount else 0 end) as revenue,
        count(*) as order_line_count
    from {{ ref('int_order_lines_enriched') }}
    group by product_id, product_name, category

)

select
    s.product_id,
    s.product_name,
    s.category,
    s.units_sold,
    s.revenue,
    s.order_line_count,
    coalesce(r.return_count, 0) as return_count,
    safe_divide(coalesce(r.return_count, 0), s.order_line_count) as return_rate
from product_sales as s
left join {{ ref('int_returns_by_product') }} as r
    on s.product_id = r.product_id