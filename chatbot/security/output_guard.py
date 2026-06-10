class OutputGuard:

    def validate(self, result: dict) -> dict:
        route = result.get("route")
        error = result.get("error")

        if error:
            return {
                "approved": True,
                "feedback": ["Response contains an explicit error state."],
            }

        if route == "sql":
            if not result.get("sql") or not result.get("rows"):
                return {
                    "approved": False,
                    "feedback": ["SQL route requires SQL query and result rows."],
                }

        if route == "rag":
            if not result.get("sources"):
                return {
                    "approved": False,
                    "feedback": ["RAG route requires supporting sources."],
                }

        if route == "hybrid":
            if not result.get("sql") or not result.get("rows") or not result.get("sources"):
                return {
                    "approved": False,
                    "feedback": ["Hybrid route requires SQL evidence and RAG sources."],
                }

        if not result.get("answer"):
            return {
                "approved": False,
                "feedback": ["Response answer is empty."],
            }

        return {
            "approved": True,
            "feedback": [],
        }