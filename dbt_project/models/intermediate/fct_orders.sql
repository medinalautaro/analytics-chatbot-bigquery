{{ config(
    materialized='table',
    partition_by={
        "field": "order_date",
        "data_type": "date"
    },
    cluster_by=["customer_id", "order_status"]
) }}

select
    order_id,
    customer_id,
    order_timestamp,
    date(order_timestamp) as order_date,
    order_status,
    payment_method,
    country,
    device_type,
    marketing_channel,
    subtotal_amount,
    shipping_amount,
    total_amount
from {{ ref('stg_orders') }}