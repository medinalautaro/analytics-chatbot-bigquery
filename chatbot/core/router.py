from chatbot.core.types import RouteType


SQL_KEYWORDS = {
    "revenue",
    "sales",
    "order",
    "orders",
    "count",
    "total",
    "avg",
    "average",
    "aov",
    "top channel",
    "top channels",
    "best channel",
    "best channels",
    "channel performance",
    "last month",
    "previous month",
    "prior month",
    "month before",
    "yesterday",
    "by month",
    "trend",
    "by day",
}

RAG_KEYWORDS = {
    "what is",
    "define",
    "definition",
    "meaning",
    "explain",
    "how does",
    "how is",
    "what does",
    "which model",
    "which table",
    "what table",
    "dag",
    "pipeline",
    "documentation",
    "schema",
    "metric",
    "lineage",
    "source",
}


"""def decide_route(question: str) -> RouteType:
    q = question.lower().strip()

    # Definition/explanation questions should prefer RAG unless they clearly mix with analytics
    if any(phrase in q for phrase in ["what does", "what is", "define", "definition", "meaning", "explain"]):
        if not any(phrase in q for phrase in [
            "last month", "previous month", "prior month", "month before",
            "yesterday", "by month", "trend", "top channel", "top channels",
            "best channel", "best channels"
        ]):
            return RouteType.RAG

    has_sql = any(keyword in q for keyword in SQL_KEYWORDS)
    has_rag = any(keyword in q for keyword in RAG_KEYWORDS)

    # explicit top N channel patterns should always be SQL
    import re
    if re.search(r"\btop\s+\d+\s+channels?\b", q):
        return RouteType.SQL

    if has_sql and has_rag:
        return RouteType.HYBRID
    if has_sql:
        return RouteType.SQL
    return RouteType.RAG"""

def decide_route(question: str) -> RouteType:
    q = question.lower().strip()

    def is_definition_question(q: str) -> bool:
        patterns = ["what is", "define", "meaning of"]
        return any(p in q for p in patterns)


    def has_analytics_intent(q: str) -> bool:
        patterns = ["last", "month", "top", "trend", "by", "yesterday"]
        return any(p in q for p in patterns)


    if is_definition_question(q) and not has_analytics_intent(q):
        return RouteType.RAG

    has_definition_phrase = any(
        phrase in q for phrase in [
            "what does", "what is", "define", "definition", "meaning", "explain"
        ]
    )

    has_sql = any(keyword in q for keyword in SQL_KEYWORDS)
    has_rag = any(keyword in q for keyword in RAG_KEYWORDS)

    import re
    if re.search(r"\btop\s+\d+\s+channels?\b", q):
        return RouteType.SQL

    # If both analytics and definition intent are present, force hybrid
    if has_definition_phrase and has_sql:
        return RouteType.HYBRID

    # Pure definition/explanation without analytics
    if has_definition_phrase and not has_sql:
        return RouteType.RAG

    if has_sql and has_rag:
        return RouteType.HYBRID
    if has_sql:
        return RouteType.SQL
    return RouteType.RAG