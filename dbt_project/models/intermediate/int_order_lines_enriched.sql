select
    oi.order_item_id,
    oi.order_id,
    oi.product_id,
    p.product_name,
    p.category,
    oi.quantity,
    oi.unit_price,
    oi.line_amount,
    o.order_date,
    o.order_status,
    o.customer_id,
    o.country,
    o.device_type,
    o.marketing_channel
from {{ source('raw', 'order_items') }} as oi
left join {{ ref('stg_products') }} as p
    on oi.product_id = p.product_id
left join {{ ref('fct_orders') }} as o
    on oi.order_id = o.order_id