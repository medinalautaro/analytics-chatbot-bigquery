class VerifierAgent:

    def verify(
        self,
        answer: str,
        sources: list | None = None,
        sql: str | None = None,
        rows: list | None = None,
    ) -> dict:

        approved = True
        feedback = []

        if not answer:
            approved = False
            feedback.append("Empty answer")

        has_rag_sources = sources is not None and len(sources) > 0
        has_sql_evidence = bool(sql) and rows is not None and len(rows) > 0

        if not has_rag_sources and not has_sql_evidence:
            feedback.append("No supporting evidence available")

        return {
            "approved": approved,
            "feedback": feedback,
        }