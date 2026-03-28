select
    max(order_date) as latest_order_date,
    date_sub(max(order_date), interval 1 day) as previous_order_date,
    date_trunc(max(order_date), month) as latest_order_month,
    date_sub(date_trunc(max(order_date), month), interval 1 month) as previous_order_month
from {{ ref('fct_orders') }}
where order_status = 'completed'