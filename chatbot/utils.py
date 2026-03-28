from __future__ import annotations

import pandas as pd
from google.cloud import bigquery


def run_query(project_id: str, query: str) -> pd.DataFrame:
    client = bigquery.Client(project=project_id)
    return client.query(query).to_dataframe()


def classify_question(question: str) -> str:
    q = question.lower().strip()

    if "revenue" in q and ("last month" in q or "last 30 days" in q or "total" in q):
        return "total_revenue_last_month"

    if "top products" in q or "best products" in q or "products by revenue" in q:
        return "top_products"

    if "channel" in q:
        return "channel_performance"

    return "unknown"


def explain_query_type(query_type: str) -> str:
    explanations = {
        "total_revenue_last_month": "This query calculates total revenue over the last 30 days available in the revenue mart.",
        "top_products": "This query returns the top 10 products by revenue from the product performance mart.",
        "channel_performance": "This query aggregates channel-level revenue and order counts and computes weighted average order value.",
    }
    return explanations.get(query_type, "")