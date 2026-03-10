{{ config(
    materialized='table',
    partition_by={
        "field": "order_date",
        "data_type": "date"
    },
    cluster_by=['marketing_channel']
) }}

select
    order_date,
    marketing_channel,
    count(*) as order_count,
    round(sum(total_amount), 2) as revenue,
    round(avg(total_amount), 2) as avg_order_value
from {{ ref('fct_orders') }}
where order_status = 'completed'
group by
    order_date,
    marketing_channel