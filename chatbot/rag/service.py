from chatbot.rag.simple_retriever import SimpleRetriever
from chatbot.llm.client import LLMClient
from chatbot.llm.prompts import RAG_PROMPT
import time


class RAGService:
    def __init__(self):
        self.retriever = SimpleRetriever()
        self.llm = LLMClient()

    def retrieve_sources(self, question: str, top_k: int = 3) -> list[dict]:
        return self.retriever.retrieve(question, top_k=top_k)
    
    def retrieve_sources_with_metrics(
        self,
        question: str,
        top_k: int = 3,
    ) -> dict:

        start = time.perf_counter()

        sources = self.retrieve_sources(
            question,
            top_k=top_k,
        )

        retrieval_time_ms = round(
            (time.perf_counter() - start) * 1000,
            2,
        )

        return {
            "sources": sources,
            "rag_retrieval_time_ms": retrieval_time_ms,
        }

    def answer(self, question: str) -> dict:
        sources = self.retrieve_sources(question, top_k=3)

        if not sources:
            return {
                "question": question,
                "query_name": None,
                "sql": None,
                "rows": [],
                "answer": "I could not find relevant project documentation for that question.",
                "sources": [],
                "route": "rag",
            }

        context = "\n\n".join(
            f"[SOURCE: {src['source_name']}]\n{src['snippet']}"
            for src in sources
        )

        prompt = RAG_PROMPT.format(
            question=question,
            context=context
        )

        answer = self.llm.generate(prompt)

        return {
            "question": question,
            "query_name": None,
            "sql": None,
            "rows": [],
            "answer": answer,
            "sources": sources,
            "route": "rag",
        }