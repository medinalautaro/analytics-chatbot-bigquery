# Warehouse Schema Catalog

## chatbot_revenue_monthly
Contains one row per month with:
- order_month
- order_count
- revenue
- avg_order_value

## chatbot_channel_performance_monthly
Contains one row per month per marketing channel with:
- order_month
- marketing_channel
- order_count
- revenue
- avg_order_value

## chatbot_orders_daily
Contains one row per day with:
- order_date
- order_count
- revenue
- avg_order_value

## max_dates
Contains anchor dates used by the chatbot:
- latest_order_date
- previous_order_date
- latest_order_month
- previous_order_month