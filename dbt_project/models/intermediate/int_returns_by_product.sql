select
    oi.product_id,
    count(r.return_id) as return_count
from {{ source('raw', 'returns') }} as r
left join {{ source('raw', 'order_items') }} as oi
    on r.order_item_id = oi.order_item_id
group by oi.product_id