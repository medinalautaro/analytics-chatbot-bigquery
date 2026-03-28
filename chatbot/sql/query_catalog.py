QUERY_CATALOG = {
    "revenue_last_month": {
        "description": "Total revenue for the month before the latest available month in the dataset.",
        "route": "sql",
        "model": "chatbot_revenue_monthly",
        "template": """
            SELECT
              order_month,
              revenue
            FROM `{{project}}.{{dataset}}.chatbot_revenue_monthly`
            WHERE order_month = (
              SELECT previous_order_month
              FROM `{{project}}.{{dataset}}.max_dates`
            )
        """,
        "patterns": [
            "revenue last month",
            "total revenue last month",
            "sales last month",
            "how much revenue last month"
        ]
    },

    "revenue_by_month": {
        "description": "Monthly revenue trend.",
        "route": "sql",
        "model": "chatbot_revenue_monthly",
        "template": """
            SELECT
              order_month,
              revenue,
              order_count,
              avg_order_value
            FROM `{{project}}.{{dataset}}.chatbot_revenue_monthly`
            ORDER BY order_month DESC
            LIMIT 12
        """,
        "patterns": [
            "revenue by month",
            "monthly revenue",
            "revenue trend",
            "monthly sales"
        ]
    },

    "revenue_last_n_months": {
        "description": "Revenue for the last N available months.",
        "route": "sql",
        "model": "chatbot_revenue_monthly",
        "template": """
            SELECT
              order_month,
              revenue,
              order_count,
              avg_order_value
            FROM `{{project}}.{{dataset}}.chatbot_revenue_monthly`
            WHERE order_month >= (
              SELECT DATE_SUB(latest_order_month, INTERVAL {months_back} MONTH)
              FROM `{{project}}.{{dataset}}.max_dates`
            )
            ORDER BY order_month DESC
        """,
        "patterns": [
            "revenue last n months",
            "revenue last months",
            "sales last months"
        ],
        "parameters": ["months_back"]
    },

    "orders_last_month": {
        "description": "Completed order count for the month before the latest available month in the dataset.",
        "route": "sql",
        "model": "chatbot_revenue_monthly",
        "template": """
            SELECT
              order_month,
              order_count
            FROM `{{project}}.{{dataset}}.chatbot_revenue_monthly`
            WHERE order_month = (
              SELECT previous_order_month
              FROM `{{project}}.{{dataset}}.max_dates`
            )
        """,
        "patterns": [
            "orders last month",
            "completed orders last month",
            "how many orders last month"
        ]
    },

    "aov_last_month": {
        "description": "Average order value for the month before the latest available month in the dataset.",
        "route": "sql",
        "model": "chatbot_revenue_monthly",
        "template": """
            SELECT
              order_month,
              avg_order_value
            FROM `{{project}}.{{dataset}}.chatbot_revenue_monthly`
            WHERE order_month = (
              SELECT previous_order_month
              FROM `{{project}}.{{dataset}}.max_dates`
            )
        """,
        "patterns": [
            "average order value last month",
            "avg order value last month",
            "aov last month"
        ]
    },

    "channel_performance_last_month": {
        "description": "Channel performance for the month before the latest available month in the dataset.",
        "route": "sql",
        "model": "chatbot_channel_performance_monthly",
        "template": """
            SELECT
              c.order_month,
              c.marketing_channel,
              c.revenue,
              c.order_count,
              c.avg_order_value
            FROM `{{project}}.{{dataset}}.chatbot_channel_performance_monthly` c
            WHERE c.order_month = (
              SELECT previous_order_month
              FROM `{{project}}.{{dataset}}.max_dates`
            )
            ORDER BY c.revenue DESC
        """,
        "patterns": [
            "channel performance last month",
            "revenue by channel last month",
            "channels last month",
            "marketing channel performance last month"
        ]
    },

    "top_channel_last_month": {
        "description": "Top marketing channel by revenue for the month before the latest available month in the dataset.",
        "route": "sql",
        "model": "chatbot_channel_performance_monthly",
        "template": """
            SELECT
              c.order_month,
              c.marketing_channel,
              c.revenue,
              c.order_count,
              c.avg_order_value
            FROM `{{project}}.{{dataset}}.chatbot_channel_performance_monthly` c
            WHERE c.order_month = (
              SELECT previous_order_month
              FROM `{{project}}.{{dataset}}.max_dates`
            )
            ORDER BY c.revenue DESC
            LIMIT 1
        """,
        "patterns": [
            "top channel last month",
            "best channel last month",
            "which channel performed best last month",
            "highest revenue channel last month"
        ]
    },

    "top_k_channels_last_month": {
        "description": "Top K marketing channels by revenue for the month before the latest available month in the dataset.",
        "route": "sql",
        "model": "chatbot_channel_performance_monthly",
        "template": """
            SELECT
              c.order_month,
              c.marketing_channel,
              c.revenue,
              c.order_count,
              c.avg_order_value
            FROM `{{project}}.{{dataset}}.chatbot_channel_performance_monthly` c
            WHERE c.order_month = (
              SELECT previous_order_month
              FROM `{{project}}.{{dataset}}.max_dates`
            )
            ORDER BY c.revenue DESC
            LIMIT {top_k}
        """,
        "patterns": [
            "top k channels last month",
            "top channels last month",
            "best channels last month"
        ],
        "parameters": ["top_k"]
    },

    "orders_yesterday": {
        "description": "Completed orders for the day before the latest available date in the dataset.",
        "route": "sql",
        "model": "chatbot_orders_daily",
        "template": """
            SELECT
              d.order_date,
              d.order_count
            FROM `{{project}}.{{dataset}}.chatbot_orders_daily` d
            WHERE d.order_date = (
              SELECT previous_order_date
              FROM `{{project}}.{{dataset}}.max_dates`
            )
        """,
        "patterns": [
            "orders yesterday",
            "completed orders yesterday",
            "how many orders yesterday"
        ]
    },

    "revenue_yesterday": {
        "description": "Revenue for the day before the latest available date in the dataset.",
        "route": "sql",
        "model": "chatbot_orders_daily",
        "template": """
            SELECT
              d.order_date,
              d.revenue
            FROM `{{project}}.{{dataset}}.chatbot_orders_daily` d
            WHERE d.order_date = (
              SELECT previous_order_date
              FROM `{{project}}.{{dataset}}.max_dates`
            )
        """,
        "patterns": [
            "revenue yesterday",
            "sales yesterday",
            "how much revenue yesterday"
        ]
    },

    "daily_revenue_recent": {
        "description": "Recent daily revenue trend based on the latest available data.",
        "route": "sql",
        "model": "chatbot_orders_daily",
        "template": """
            SELECT
              order_date,
              revenue,
              order_count,
              avg_order_value
            FROM `{{project}}.{{dataset}}.chatbot_orders_daily`
            ORDER BY order_date DESC
            LIMIT 14
        """,
        "patterns": [
            "daily revenue trend",
            "recent daily revenue",
            "revenue by day",
            "daily sales trend"
        ]
    },
        "revenue_previous_month": {
        "description": "Total revenue for two months before the latest available month in the dataset.",
        "route": "sql",
        "model": "chatbot_revenue_monthly",
        "template": """
            SELECT
            order_month,
            revenue
            FROM `{{project}}.{{dataset}}.chatbot_revenue_monthly`
            WHERE order_month = (
            SELECT DATE_SUB(previous_order_month, INTERVAL 1 MONTH)
            FROM `{{project}}.{{dataset}}.max_dates`
            )
        """,
        "patterns": [
            "revenue previous month",
            "revenue prior month",
            "revenue month before"
        ]
    },

    "orders_previous_month": {
        "description": "Completed order count for two months before the latest available month in the dataset.",
        "route": "sql",
        "model": "chatbot_revenue_monthly",
        "template": """
            SELECT
            order_month,
            order_count
            FROM `{{project}}.{{dataset}}.chatbot_revenue_monthly`
            WHERE order_month = (
            SELECT DATE_SUB(previous_order_month, INTERVAL 1 MONTH)
            FROM `{{project}}.{{dataset}}.max_dates`
            )
        """,
        "patterns": [
            "orders previous month",
            "orders prior month",
            "orders month before"
        ]
    },

    "aov_previous_month": {
        "description": "Average order value for two months before the latest available month in the dataset.",
        "route": "sql",
        "model": "chatbot_revenue_monthly",
        "template": """
            SELECT
            order_month,
            avg_order_value
            FROM `{{project}}.{{dataset}}.chatbot_revenue_monthly`
            WHERE order_month = (
            SELECT DATE_SUB(previous_order_month, INTERVAL 1 MONTH)
            FROM `{{project}}.{{dataset}}.max_dates`
            )
        """,
        "patterns": [
            "average order value previous month",
            "avg order value previous month",
            "aov previous month"
        ]
    },

    "top_k_channels_previous_month": {
        "description": "Top K marketing channels by revenue for two months before the latest available month in the dataset.",
        "route": "sql",
        "model": "chatbot_channel_performance_monthly",
        "template": """
            SELECT
            c.order_month,
            c.marketing_channel,
            c.revenue,
            c.order_count,
            c.avg_order_value
            FROM `{{project}}.{{dataset}}.chatbot_channel_performance_monthly` c
            WHERE c.order_month = (
            SELECT DATE_SUB(previous_order_month, INTERVAL 1 MONTH)
            FROM `{{project}}.{{dataset}}.max_dates`
            )
            ORDER BY c.revenue DESC
            LIMIT {top_k}
        """,
        "patterns": [
            "top k channels previous month",
            "top channels previous month",
            "best channels previous month"
        ],
        "parameters": ["top_k"]
    },
}