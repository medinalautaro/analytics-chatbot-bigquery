from __future__ import annotations

QUERY_TEMPLATES = {
    "total_revenue_last_month": """
        WITH max_date AS (
            SELECT MAX(order_date) AS max_order_date
            FROM `{project_id}.staging.mart_revenue_daily`
        )
        SELECT
            ROUND(SUM(revenue), 2) AS total_revenue
        FROM `{project_id}.staging.mart_revenue_daily`, max_date
        WHERE order_date >= DATE_SUB(max_order_date, INTERVAL 30 DAY)
    """,
    "top_products": """
        SELECT
            product_name,
            category,
            ROUND(revenue, 2) AS revenue,
            units_sold,
            ROUND(return_rate, 4) AS return_rate
        FROM `{project_id}.staging.mart_product_performance`
        ORDER BY revenue DESC
        LIMIT 10
    """,
    "channel_performance": """
        SELECT
            marketing_channel,
            ROUND(SUM(revenue), 2) AS revenue,
            SUM(order_count) AS order_count,
            ROUND(SAFE_DIVIDE(SUM(revenue), SUM(order_count)), 2) AS avg_order_value
        FROM `{project_id}.staging.mart_channel_performance`
        GROUP BY marketing_channel
        ORDER BY revenue DESC
    """,
}