from sentence_transformers import CrossEncoder


RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"


class Reranker:
    def __init__(self):
        self.model = CrossEncoder(RERANKER_MODEL)

    def rerank(self, question: str, documents: list[dict], top_k: int = 3):
        if not documents:
            return []

        pairs = [(question, doc["snippet"]) for doc in documents]
        scores = self.model.predict(pairs)

        ranked = []

        for doc, score in zip(documents, scores):
            item = dict(doc)
            item["rerank_score"] = round(float(score), 4)
            ranked.append(item)

        ranked.sort(key=lambda x: x["rerank_score"], reverse=True)

        return ranked[:top_k]