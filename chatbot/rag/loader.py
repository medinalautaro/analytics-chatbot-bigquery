from pathlib import Path

ALLOWED_EXTENSIONS = {".md", ".sql", ".yml", ".yaml", ".py"}


def load_documents(base_paths: list[str]) -> list[dict]:
    documents = []

    for base_path in base_paths:
        base = Path(base_path)
        print(f"[RAG] Checking path: {base.resolve()} | exists={base.exists()}")

        if not base.exists():
            continue

        for path in base.rglob("*"):
            if path.is_file() and path.suffix.lower() in ALLOWED_EXTENSIONS:
                try:
                    text = path.read_text(encoding="utf-8", errors="ignore")
                    documents.append(
                        {
                            "source_name": str(path).replace("\\", "/"),
                            "text": text,
                        }
                    )
                except Exception:
                    continue

    print(f"[RAG] Total loaded documents: {len(documents)}")
    return documents