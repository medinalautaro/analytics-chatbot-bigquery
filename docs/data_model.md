# Data Model

## Raw tables

### customers
- One row per customer.
- Contains customer registration and profile information.
- Referenced by orders through customer_id.

### orders
- One row per order.
- Represents a purchase made by a customer.
- Linked to customers, payments, shipments, and order_items.

### order_items
- One row per product within an order.
- Represents the products purchased in each order.
- Linked to orders through order_id.

### payments
- One row per payment event.
- Stores payment information associated with orders.
- Multiple payment records may exist for a single order.

### shipments
- One row per shipment.
- Stores fulfillment and delivery information.
- Linked to orders through order_id.

### returns
- One row per returned order item.
- Stores information about product returns.
- Linked to order_items.

### marketing_spend
- One row per date and channel.
- Stores marketing investment data.
- Independent from transactional tables.

---

## Core marts

### mart_revenue_daily
- One row per date.
- Aggregated daily business activity.
- Intended for revenue trend analysis.

### mart_channel_performance
- One row per date and channel.
- Aggregated marketing channel performance.
- Combines marketing and sales information.

### mart_product_performance
- One row per product.
- Aggregated product-level performance.
- Used for product ranking and analysis.

### mart_customer_retention
- One row per cohort month and retention month.
- Aggregated customer retention information.
- Used for cohort analysis.
