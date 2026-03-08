select
    order_id,
    customer_id,
    cast(order_timestamp as timestamp) as order_timestamp,
    order_status,
    payment_method,
    country,
    coalesce(device_type, 'unknown') as device_type,
    coalesce(marketing_channel, 'unknown') as marketing_channel,
    subtotal_amount,
    shipping_amount,
    total_amount
from {{ source('raw', 'orders') }}