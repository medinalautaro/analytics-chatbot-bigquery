select
    'revenue' as metric_name,
    'Sum of total_amount for completed orders.' as definition,
    'chatbot_revenue_monthly' as source_model,
    'sum(total_amount)' as calculation,
    'order_status = completed' as filters_applied,
    'Monthly in chatbot_revenue_monthly; daily in chatbot_orders_daily.' as grain_notes,
    'Excludes orders not marked as completed.' as caveats

union all

select
    'order_count' as metric_name,
    'Count of completed orders.' as definition,
    'chatbot_revenue_monthly' as source_model,
    'count(*)' as calculation,
    'order_status = completed' as filters_applied,
    'Monthly in chatbot_revenue_monthly; daily in chatbot_orders_daily; monthly by channel in chatbot_channel_performance_monthly.' as grain_notes,
    'Counts rows in fct_orders after filtering to completed status.' as caveats

union all

select
    'avg_order_value' as metric_name,
    'Average total_amount for completed orders.' as definition,
    'chatbot_revenue_monthly' as source_model,
    'avg(total_amount)' as calculation,
    'order_status = completed' as filters_applied,
    'Available at monthly, daily, and monthly-by-channel grain depending on model.' as grain_notes,
    'Average depends on the aggregation grain of the selected model.' as caveats