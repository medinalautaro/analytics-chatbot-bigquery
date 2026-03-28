from chatbot.core.router import decide_route
from chatbot.core.types import RouteType
from chatbot.core.decompose import decompose_hybrid_question
from chatbot.core.memory import MemoryStore
from chatbot.core.followup import is_followup_question, resolve_followup
from chatbot.core.history import HistoryStore
from chatbot.sql.executor import SQLExecutor
from chatbot.llm.client import LLMClient
from chatbot.llm.prompts import SQL_ANSWER_PROMPT, HYBRID_PROMPT
from chatbot.rag.service import RAGService
from chatbot.core.config import settings
from cachetools import TTLCache
import json

response_cache = TTLCache(maxsize=200, ttl=300)  # 5 minutes

def make_cache_key(message: str, history) -> str:
    return json.dumps(
        {"message": message.strip().lower(), "history": history},
        sort_keys=True,
        ensure_ascii=False,
    )

class ChatService:
    def __init__(self):
        self.sql_executor = SQLExecutor()
        self.llm = LLMClient()
        self.rag_service = RAGService()
        self.memory = MemoryStore()
        self.history = HistoryStore()

    def _history_payload(self) -> list[dict]:
        items = self.history.get_history()
        payload = []

        for item in items:
            user_question = item.get("user_question")
            answer = item.get("answer")

            if user_question:
                payload.append({"role": "user", "content": user_question})
            if answer:
                payload.append({"role": "assistant", "content": answer})

        return payload

    def _response(
        self,
        *,
        question: str,
        resolved_question: str,
        answer: str,
        route: str,
        query_name: str | None = None,
        sql: str | None = None,
        rows: list | None = None,
        sources: list | None = None,
        error: str | None = None,
        **extra,
    ) -> dict:
        result = {
            "question": question,
            "resolved_question": resolved_question,
            "query_name": query_name,
            "sql": sql,
            "rows": rows or [],
            "answer": answer,
            "error": error,
            "route": route,
            "sources": sources or [],
            "history": self._history_payload(),
        }
        result.update(extra)
        return result

    def answer(self, question: str) -> dict:
        original_question = (question or "").strip()
        if not original_question:
            return self._response(
                question="",
                resolved_question="",
                query_name=None,
                sql=None,
                rows=[],
                answer="Please enter a question before sending.",
                error="EMPTY_MESSAGE",
                route="unknown",
                sources=[],
            )

        try:
            settings.validate()
        except ValueError:
            return self._response(
                question=original_question,
                resolved_question=original_question,
                query_name=None,
                sql=None,
                rows=[],
                answer="The server is missing required configuration. Check environment variables before running the app.",
                error="CONFIG_MISSING",
                route="unknown",
                sources=[],
            )

        history_payload = self._history_payload()
        cache_key = make_cache_key(original_question, history_payload)

        cached = response_cache.get(cache_key)
        if cached is not None:
            return cached

        state = self.memory.get_state()
        question = original_question

        try:
            route = decide_route(question)
        except Exception:
            result = self._response(
                question=original_question,
                resolved_question=question,
                query_name=None,
                sql=None,
                rows=[],
                answer="I couldn't determine how to answer that question.",
                error="ROUTING_FAILED",
                route="unknown",
                sources=[],
            )
            self._update_history(original_question, result)
            return result

        if route == RouteType.RAG:
            try:
                result = self.rag_service.answer(question)
                result["resolved_question"] = question

                if not result.get("sources"):
                    result = self._response(
                        question=original_question,
                        resolved_question=question,
                        query_name=None,
                        sql=None,
                        rows=[],
                        answer="I couldn't find supporting documentation for that question in the current knowledge base.",
                        error="NO_RAG_SOURCES",
                        route=route.value,
                        sources=[],
                    )
                else:
                    result["history"] = self._history_payload()

                self._update_memory(original_question, route.value, result)
                self._update_history(original_question, result)
                response_cache[cache_key] = result
                return result

            except Exception:
                result = self._response(
                    question=original_question,
                    resolved_question=question,
                    query_name=None,
                    sql=None,
                    rows=[],
                    answer="I couldn't retrieve documentation context for that question.",
                    error="RAG_ANSWER_FAILED",
                    route=route.value,
                    sources=[],
                )
                self._update_history(original_question, result)
                return result

        if route == RouteType.SQL:
            sql_question = question
            if is_followup_question(sql_question):
                sql_question = resolve_followup(sql_question, state)

            result = self._answer_sql(sql_question, route.value)
            self._update_memory(original_question, route.value, result)
            self._update_history(original_question, result)

            if result.get("error") not in {"BIGQUERY_EXECUTION_FAILED", "SQL_SUMMARY_FAILED"}:
                response_cache[cache_key] = result

            return result

        if route == RouteType.HYBRID:
            result = self._answer_hybrid(question, state)
            self._update_memory(original_question, route.value, result)
            self._update_history(original_question, result)

            if result.get("error") not in {"BIGQUERY_EXECUTION_FAILED", "HYBRID_ANSWER_FAILED"}:
                response_cache[cache_key] = result

            return result

        result = self._response(
            question=original_question,
            resolved_question=question,
            query_name=None,
            sql=None,
            rows=[],
            answer="Could not determine a valid route.",
            error="UNKNOWN_ROUTE",
            route="unknown",
            sources=[],
        )
        self._update_history(original_question, result)
        response_cache[cache_key] = result
        return result

    def _answer_sql(self, question: str, route_value: str) -> dict:
        try:
            sql_result = self.sql_executor.run(question)

        except ValueError as e:
            msg = str(e)

            if "Forbidden SQL operation" in msg or "approved chatbot models" in msg:
                user_msg = "That request would produce SQL that is not allowed. Try a read-only metric question like revenue, orders, or channel performance."
                error_code = "SQL_GENERATION_FAILED"

            elif "No approved query pattern" in msg:
                user_msg = "I couldn’t confidently map that question to a supported metric or table yet. Try asking about revenue, orders, AOV, or channel performance."
                error_code = "NO_SQL_MATCH"

            else:
                user_msg = "I couldn’t map that question to an approved analytics query yet."
                error_code = "NO_SQL_MATCH"

            return self._response(
                question=question,
                resolved_question=question,
                query_name=None,
                sql=None,
                rows=[],
                answer=user_msg,
                error=error_code,
                route=route_value,
                sources=[],
            )

        except Exception:
            return self._response(
                question=question,
                resolved_question=question,
                query_name=None,
                sql=None,
                rows=[],
                answer="I generated an analytics request, but executing it failed.",
                error="BIGQUERY_EXECUTION_FAILED",
                route=route_value,
                sources=[],
            )

        if not sql_result.rows:
            return self._response(
                question=question,
                resolved_question=question,
                query_name=sql_result.query_name,
                sql=sql_result.sql,
                rows=[],
                answer="The query ran successfully, but returned no rows for that time range or filter.",
                error="EMPTY_RESULT",
                route=route_value,
                sources=[],
            )

        prompt = SQL_ANSWER_PROMPT.format(
            question=question,
            query_name=sql_result.query_name,
            rows=sql_result.rows
        )

        try:
            answer = self.llm.generate(prompt)
        except Exception:
            return self._response(
                question=question,
                resolved_question=question,
                query_name=sql_result.query_name,
                sql=sql_result.sql,
                rows=sql_result.rows,
                answer="I ran the query, but failed to generate a natural-language summary.",
                error="SQL_SUMMARY_FAILED",
                route=route_value,
                sources=[],
            )

        return self._response(
            question=question,
            resolved_question=question,
            query_name=sql_result.query_name,
            sql=sql_result.sql,
            rows=sql_result.rows,
            answer=answer,
            error=None,
            route=route_value,
            sources=[],
        )

    def _answer_hybrid(self, question: str, state) -> dict:
        parts = decompose_hybrid_question(question)
        sql_question = parts["sql_question"]
        rag_question = parts["rag_question"]

        if is_followup_question(sql_question):
            sql_question = resolve_followup(sql_question, state)

        try:
            sql_result = self.sql_executor.run(sql_question)

        except ValueError:
            return self._response(
                question=question,
                resolved_question=question,
                query_name=None,
                sql=None,
                rows=[],
                answer="I detected a hybrid question, but couldn't run the analytics portion safely.",
                error="NO_SQL_MATCH",
                route="hybrid",
                sources=[],
                decomposition=parts,
            )

        except Exception:
            return self._response(
                question=question,
                resolved_question=question,
                query_name=None,
                sql=None,
                rows=[],
                answer="I detected a hybrid question, but couldn't run the analytics portion.",
                error="BIGQUERY_EXECUTION_FAILED",
                route="hybrid",
                sources=[],
                decomposition=parts,
            )

        retrieval_error = None
        try:
            sources = self.rag_service.retrieve_sources(rag_question, top_k=3)
        except Exception as e:
            sources = []
            retrieval_error = str(e)

        context = "\n\n".join(
            f"[SOURCE: {src['source_name']}]\n{src['snippet']}"
            for src in sources
        ) if sources else "No relevant documentation sources were retrieved."

        prompt = HYBRID_PROMPT.format(
            question=question,
            query_name=sql_result.query_name,
            rows=sql_result.rows,
            context=context
        )

        try:
            answer = self.llm.generate(prompt)
        except Exception:
            error_code = "HYBRID_ANSWER_FAILED"
            if retrieval_error and not sources:
                error_code = "NO_RAG_SOURCES"

            return self._response(
                question=question,
                resolved_question=question,
                query_name=sql_result.query_name,
                sql=sql_result.sql,
                rows=sql_result.rows,
                answer="I ran the query, but failed to generate the final answer.",
                error=error_code,
                route="hybrid",
                sources=sources,
                decomposition=parts,
            )

        result = self._response(
            question=question,
            resolved_question=question,
            query_name=sql_result.query_name,
            sql=sql_result.sql,
            rows=sql_result.rows,
            answer=answer,
            error="NO_RAG_SOURCES" if not sources else None,
            route="hybrid",
            sources=sources,
            decomposition=parts,
        )
        return result

    def _update_memory(self, original_question: str, route_value: str, result: dict) -> None:
        query_name = result.get("query_name")

        metric = None
        timeframe = None
        top_k = None

        if query_name:
            if "revenue" in query_name:
                metric = "revenue"
            elif "orders" in query_name:
                metric = "orders"
            elif "aov" in query_name:
                metric = "avg_order_value"
            elif "channel" in query_name:
                metric = "top_channels"

            if "last_month" in query_name:
                timeframe = "last month"
            elif "previous_month" in query_name:
                timeframe = "previous month"
            elif "yesterday" in query_name:
                timeframe = "yesterday"

        if result.get("rows") and query_name in {"top_k_channels_last_month", "top_k_channels_previous_month"}:
            top_k = len(result["rows"])

        self.memory.update(
            last_user_question=original_question,
            last_route=route_value,
            last_query_name=query_name,
            last_metric=metric,
            last_timeframe=timeframe,
            last_top_k=top_k,
            last_result_summary=result.get("answer"),
        )

    def _update_history(self, original_question: str, result: dict) -> None:
        self.history.add(
            user_question=original_question,
            resolved_question=result.get("resolved_question"),
            route=result.get("route"),
            query_name=result.get("query_name"),
            sql=result.get("sql"),
            answer=result.get("answer"),
        )