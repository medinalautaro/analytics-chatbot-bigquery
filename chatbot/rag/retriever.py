"""class Retriever:
    def retrieve(self, question: str) -> list[dict]:
        # Placeholder retrieval
        return [
            {
                "source_name": "docs/placeholder.md",
                "snippet": "No real RAG retrieval is connected yet."
            }
        ]"""

import pickle
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


INDEX_DIR = Path("chatbot/rag/index")
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


class Retriever:
    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL)
        self.index = faiss.read_index(str(INDEX_DIR / "docs.faiss"))

        with open(INDEX_DIR / "records.pkl", "rb") as f:
            self.records = pickle.load(f)

    def retrieve(self, question: str, top_k: int = 10) -> list[dict]:
        query_embedding = self.model.encode(
            [question],
            normalize_embeddings=True,
        )

        query_embedding = np.array(query_embedding).astype("float32")

        scores, indices = self.index.search(query_embedding, top_k)

        results = []

        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue

            record = self.records[idx]

            results.append({
                "source_name": record.get("source_name", record.get("source")),
                "chunk_id": record["chunk_id"],
                "snippet": record["text"],
                "retrieval_score": round(float(score), 4),
            })

        return results