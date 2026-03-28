select
    'chatbot_revenue_monthly' as model_name,
    'Monthly revenue, completed order count, and average order value.' as description,
    'one row per month' as grain,
    'order_month' as dimensions,
    'revenue, order_count, avg_order_value' as measures,
    'Use for monthly KPI and trend questions.' as intended_use,
    'What was total revenue last month?' as example_question

union all

select
    'chatbot_channel_performance_monthly' as model_name,
    'Monthly channel-level performance for completed orders.' as description,
    'one row per month per marketing_channel' as grain,
    'order_month, marketing_channel' as dimensions,
    'revenue, order_count, avg_order_value' as measures,
    'Use for channel comparison questions.' as intended_use,
    'Which channel performed best last month?' as example_question

union all

select
    'chatbot_orders_daily' as model_name,
    'Daily completed order metrics.' as description,
    'one row per day' as grain,
    'order_date' as dimensions,
    'revenue, order_count, avg_order_value' as measures,
    'Use for recent operational and daily trend questions.' as intended_use,
    'How many completed orders did we have yesterday?' as example_question