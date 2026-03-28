import re
from chatbot.rag.loader import load_documents


class SimpleRetriever:
    def __init__(self):
        self.documents = load_documents(
            [
                "dbt/models",
                "docs",
                "airflow/dags",
                "chatbot",
            ]
        )

    @staticmethod
    def _tokenize(text: str) -> set[str]:
        return set(re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", text.lower()))

    @staticmethod
    def _expand_query_tokens(tokens: set[str]) -> set[str]:
        expanded = set(tokens)

        synonyms = {
            "revenue": {"sales", "total_amount", "metric", "definition"},
            "avg_order_value": {"aov", "average", "avg", "order", "value"},
            "chatbot_revenue_monthly": {"revenue", "monthly", "order_month"},
            "chatbot_channel_performance_monthly": {"channel", "monthly", "marketing_channel"},
            "chatbot_orders_daily": {"orders", "daily", "order_date"},
            "contain": {"contains", "columns", "fields", "description", "model"},
            "mean": {"definition", "meaning", "metric", "describe"},
        }

        for token in list(tokens):
            if token in synonyms:
                expanded.update(synonyms[token])

        return expanded

    def retrieve(self, question: str, top_k: int = 5) -> list[dict]:
        q_tokens = self._tokenize(question)
        q_tokens = self._expand_query_tokens(q_tokens)

        scored = []

        for doc in self.documents:
            text = doc["text"]
            source_name = doc["source_name"]

            d_tokens = self._tokenize(text)
            path_tokens = self._tokenize(source_name)

            content_overlap = q_tokens.intersection(d_tokens)
            path_overlap = q_tokens.intersection(path_tokens)

            score = len(content_overlap) + (2 * len(path_overlap))

            for token in q_tokens:
                if token in source_name.lower():
                    score += 5

            if score > 0:
                snippet = self._best_snippet(text, q_tokens)
                scored.append(
                    {
                        "source_name": source_name,
                        "snippet": snippet,
                        "score": score,
                    }
                )

        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top_k]

    def _best_snippet(self, text: str, q_tokens: set[str], window: int = 700) -> str:
        lowered = text.lower()

        best_pos = 0
        best_hits = -1

        if len(text) <= window:
            return text.strip()

        for i in range(0, max(1, len(text) - window), max(100, window // 5)):
            chunk = lowered[i:i + window]
            hits = sum(1 for token in q_tokens if token in chunk)
            if hits > best_hits:
                best_hits = hits
                best_pos = i

        snippet = text[best_pos:best_pos + window].strip()
        return snippet.replace("\n\n", "\n")