{{ config(
    materialized='table',
    partition_by={
        "field": "order_date",
        "data_type": "date"
    }
) }}

SELECT
    DATE(order_timestamp) AS order_date,
    COUNT(*) AS order_count,
    SUM(total_amount) AS revenue,
    AVG(total_amount) AS avg_order_value
FROM {{ ref('stg_orders') }}
WHERE order_status = 'completed'
GROUP BY order_date