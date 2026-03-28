from chatbot.sql.query_catalog import QUERY_CATALOG


def normalize_text(text: str) -> str:
    return " ".join(text.lower().strip().split())


def match_query(question: str) -> str:
    q = normalize_text(question)

    # Parameterized intents first
    if "revenue" in q and "last" in q and "month" in q:
        import re
        if re.search(r"last\s+\d+\s+months?", q):
            return "revenue_last_n_months"

    if ("top" in q and "channel" in q and "last month" in q):
        import re
        if re.search(r"top\s+\d+", q):
            return "top_k_channels_last_month"

    # Exact pattern matching from catalog
    for query_name, entry in QUERY_CATALOG.items():
        for pattern in entry.get("patterns", []):
            if pattern in q:
                return query_name

    # Fallback rules
    if "revenue" in q and "last month" in q:
        return "revenue_last_month"

    if "revenue" in q and ("by month" in q or "monthly" in q or "trend" in q):
        return "revenue_by_month"

    if "orders" in q and "last month" in q:
        return "orders_last_month"
    
    if "revenue" in q and ("previous month" in q or "prior month" in q or "month before" in q):
        return "revenue_previous_month"

    if "orders" in q and ("previous month" in q or "prior month" in q or "month before" in q):
        return "orders_previous_month"

    if ("avg order value" in q or "average order value" in q or "aov" in q) and (
        "previous month" in q or "prior month" in q or "month before" in q
    ):
        return "aov_previous_month"

    if "channel" in q and ("previous month" in q or "prior month" in q or "month before" in q):
        import re
        if re.search(r"top\s+\d+", q):
            return "top_k_channels_previous_month"

    if ("avg order value" in q or "average order value" in q or "aov" in q) and "last month" in q:
        return "aov_last_month"

    if ("top channel" in q or "best channel" in q or "highest revenue channel" in q) and "last month" in q:
        return "top_channel_last_month"

    if "channel" in q and "last month" in q:
        return "channel_performance_last_month"

    if "orders" in q and "yesterday" in q:
        return "orders_yesterday"

    if "revenue" in q and "yesterday" in q:
        return "revenue_yesterday"

    raise ValueError("No approved query pattern matched the question.")