# Metrics

## revenue
Revenue is defined as the sum of `total_amount` for orders with `order_status = 'completed'`.

## order_count
Order count is the number of orders with `order_status = 'completed'`.

## avg_order_value
Average order value is defined as the average of `total_amount` for orders with `order_status = 'completed'`.

## chatbot_orders_daily
This model contains one row per day with:
- `order_date`
- `order_count`
- `revenue`
- `avg_order_value`


## chatbot_revenue_monthly
This model is used for monthly KPI questions like:
- revenue last month
- revenue last 3 months
- average order value last month

## chatbot_channel_performance_monthly
This model is used for channel ranking and comparison questions like:
- top 3 channels last month
- best channel last month
- revenue by channel last month

# Channel Attribution

Channel attribution is the process of assigning orders, revenue, or customer conversions to the marketing or acquisition channel that generated them.

In this project, channel performance is evaluated using order count, revenue, and average order value grouped by marketing channel.

The chatbot uses the `chatbot_channel_performance_monthly` model to answer questions such as:
- top channels last month
- best channel last month
- revenue by channel