import re


SQL_HINTS = [
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
    "best channel",
    "last month",
    "yesterday",
    "by month",
    "trend",
    "by day",
]

RAG_HINTS = [
    "what is",
    "what does",
    "define",
    "definition",
    "meaning",
    "explain",
    "how is",
    "how does",
    "which model",
    "which table",
    "what model",
    "what table",
    "contains",
    "calculated",
    "calculation",
    "metric",
]


def _normalize(text: str) -> str:
    return " ".join(text.lower().strip().split())


def _split_clauses(question: str) -> list[str]:
    q = question.strip()

    # Split on common conjunctions while preserving useful clauses
    parts = re.split(
        r"\b(?:and|also|plus)\b|,",
        q,
        flags=re.IGNORECASE
    )

    cleaned = [part.strip(" .?") for part in parts if part.strip(" .?")]
    return cleaned


def _score_sql(clause: str) -> int:
    c = _normalize(clause)
    return sum(1 for hint in SQL_HINTS if hint in c)


def _score_rag(clause: str) -> int:
    c = _normalize(clause)
    return sum(1 for hint in RAG_HINTS if hint in c)


def decompose_hybrid_question(question: str) -> dict:
    clauses = _split_clauses(question)

    sql_candidates = []
    rag_candidates = []

    for clause in clauses:
        sql_score = _score_sql(clause)
        rag_score = _score_rag(clause)

        if sql_score > 0:
            sql_candidates.append((clause, sql_score))
        if rag_score > 0:
            rag_candidates.append((clause, rag_score))

    sql_candidates.sort(key=lambda x: x[1], reverse=True)
    rag_candidates.sort(key=lambda x: x[1], reverse=True)

    sql_question = sql_candidates[0][0] if sql_candidates else question
    rag_question = rag_candidates[0][0] if rag_candidates else question

    return {
        "sql_question": sql_question,
        "rag_question": rag_question,
        "clauses": clauses,
    }