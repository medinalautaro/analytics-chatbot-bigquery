# Data Model

## Raw tables
- customers: one row per customer
- orders: one row per order
- order_items: one row per product within an order
- payments: one row per payment event
- shipments: one row per shipment
- returns: one row per returned order item
- marketing_spend: one row per date and channel

## Core marts
- mart_revenue_daily: one row per date
- mart_channel_performance: one row per date and channel
- mart_product_performance: one row per product
- mart_customer_retention: one row per cohort month and retention month