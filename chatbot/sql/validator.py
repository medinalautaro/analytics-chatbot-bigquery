FORBIDDEN_TOKENS = {
    "insert", "update", "delete", "drop", "alter", "merge", "truncate"
}

APPROVED_MODELS = {
    "chatbot_revenue_monthly",
    "chatbot_channel_performance_monthly",
    "chatbot_orders_daily",
}


def validate_sql(sql: str) -> None:
    lowered = sql.lower()

    if any(token in lowered for token in FORBIDDEN_TOKENS):
        raise ValueError("Forbidden SQL operation detected.")

    if not any(model in lowered for model in APPROVED_MODELS):
        raise ValueError("SQL must only target approved chatbot models.")