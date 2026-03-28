{{ config(
    materialized='table',
    partition_by={
      "field": "order_month",
      "data_type": "date"
    }
) }}

select
    date_trunc(order_date, month) as order_month,
    count(*) as order_count,
    round(sum(total_amount), 2) as revenue,
    round(avg(total_amount), 2) as avg_order_value
from {{ ref('fct_orders') }}
where order_status = 'completed'
group by order_month