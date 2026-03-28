{{ config(
    materialized='table',
    partition_by={
      "field": "order_month",
      "data_type": "date"
    },
    cluster_by=["marketing_channel"]
) }}

select
    date_trunc(order_date, month) as order_month,
    marketing_channel,
    count(*) as order_count,
    round(sum(total_amount), 2) as revenue,
    round(avg(total_amount), 2) as avg_order_value
from {{ ref('fct_orders') }}
where order_status = 'completed'
group by order_month, marketing_channel