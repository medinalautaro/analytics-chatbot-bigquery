from chatbot.rag.retriever import Retriever
from chatbot.llm.client import LLMClient
from chatbot.llm.prompts import RAG_PROMPT
from chatbot.rag.reranker import Reranker
import time


class RAGService:
    def __init__(self):
        self.retriever = Retriever()
        self.llm = LLMClient()
        self.reranker = Reranker()

    def retrieve_sources(
        self,
        question: str,
        retrieval_k: int = 10,
        rerank_k: int = 3,
    ) -> list[dict]:

        retrieved = self.retriever.retrieve(
            question,
            top_k=retrieval_k,
        )

        reranked = self.reranker.rerank(
            question=question,
            documents=retrieved,
            top_k=rerank_k,
        )

        return reranked
    
    def retrieve_sources_with_metrics(
        self,
        question: str,
        retrieval_k: int = 10,
        rerank_k: int = 3,
    ) -> dict:

        start = time.perf_counter()

        sources = self.retrieve_sources(
            question,
            retrieval_k=retrieval_k,
            rerank_k=rerank_k,
        )

        retrieval_time_ms = round(
            (time.perf_counter() - start) * 1000,
            2,
        )

        return {
            "sources": sources,
            "rag_retrieval_time_ms": retrieval_time_ms,
            "retrieval_k": retrieval_k,
            "rerank_k": rerank_k,
        }

    def answer(self, question: str) -> dict:
        sources = self.retrieve_sources(
            question,
            retrieval_k=10,
            rerank_k=3,
        )

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