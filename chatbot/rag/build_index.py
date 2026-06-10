from pathlib import Path
import pickle

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


DOCS_DIR = Path("docs")
INDEX_DIR = Path("chatbot/rag/index")
INDEX_DIR.mkdir(parents=True, exist_ok=True)

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def chunk_text(text: str, chunk_size: int = 700, overlap: int = 100):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks


def main():
    model = SentenceTransformer(EMBEDDING_MODEL)

    records = []

    for path in DOCS_DIR.glob("*.md"):
        text = path.read_text(encoding="utf-8")

        for i, chunk in enumerate(chunk_text(text)):
            records.append({
                "source_name": str(path),
                "chunk_id": i,
                "text": chunk,
            })

    if not records:
        raise ValueError(
            "No markdown documents were found. Add at least one .md file inside the docs/ folder."
        )

    texts = [r["text"] for r in records]

    embeddings = model.encode(texts, normalize_embeddings=True)
    embeddings = np.array(embeddings).astype("float32")

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, str(INDEX_DIR / "docs.faiss"))

    with open(INDEX_DIR / "records.pkl", "wb") as f:
        pickle.dump(records, f)

    print(f"Indexed {len(records)} chunks.")


if __name__ == "__main__":
    main()