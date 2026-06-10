import json
from datetime import datetime, timezone
from pathlib import Path


LOG_FILE = Path("logs/audit.jsonl")
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)


class AuditLogger:

    def log(self, result: dict) -> None:
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "question": result.get("question"),
            "resolved_question": result.get("resolved_question"),
            "route": result.get("route"),
            "query_name": result.get("query_name"),
            "error": result.get("error"),
            "cache_hit": result.get("cache_hit"),
            "metrics": result.get("metrics"),
            "verification": result.get("verification"),
            "output_validation": result.get("output_validation"),
            "sources_count": len(result.get("sources", [])),
            "rows_count": len(result.get("rows", [])),
        }

        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")