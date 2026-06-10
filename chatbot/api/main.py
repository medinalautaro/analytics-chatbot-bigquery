"""from fastapi import FastAPI
from pydantic import BaseModel
from chatbot.services.chat_service import ChatService

app = FastAPI(title="Hybrid Analytics Chatbot")

service = ChatService()


class ChatRequest(BaseModel):
    question: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/history")
def history():
    return {
        "history": service.history.get_history(),
        "memory": service.memory.get_state().__dict__,
    }


@app.post("/chat")
def chat(request: ChatRequest):
    return service.answer(request.question)"""

from fastapi import UploadFile, File
from chatbot.vision.classifier import ImageClassifier
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import traceback

from chatbot.schemas import ChatRequest
from chatbot.services.chat_service import ChatService
from chatbot.utils.responses import error_response

from pydantic import BaseModel
from chatbot.rag.retriever import Retriever
from chatbot.rag.reranker import Reranker

app = FastAPI(title="Analytics Chatbot API", version="1.0.0")

image_classifier = ImageClassifier()

retriever = Retriever()
reranker = Reranker()


class RagSearchRequest(BaseModel):
    question: str
    retrieval_k: int = 10
    rerank_k: int = 3

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
def chat(req: ChatRequest):
    if not req.message.strip():
        return error_response(
            answer="Please enter a question before sending.",
            error="EMPTY_MESSAGE",
            route="unknown",
            history=req.history,
        )

    try:
        chat_service = ChatService()
        return chat_service.answer(req.message)

    except Exception as e:
        print("===== UNEXPECTED ERROR IN /chat =====")
        print(repr(e))
        traceback.print_exc()

        return JSONResponse(
            status_code=500,
            content=error_response(
                answer="Something unexpected went wrong while processing your request.",
                error="UNEXPECTED_ERROR",
                route="unknown",
                history=req.history,
            ).model_dump()
        )
    
@app.post("/vision/classify")
async def classify_image(file: UploadFile = File(...), top_k: int = 5):
    image_bytes = await file.read()
    return image_classifier.predict(image_bytes=image_bytes, top_k=top_k)


@app.post("/rag/search")
def rag_search(req: RagSearchRequest):

    try:

        retrieved = retriever.retrieve(
            question=req.question,
            top_k=req.retrieval_k,
        )

        reranked = reranker.rerank(
            question=req.question,
            documents=retrieved,
            top_k=req.rerank_k,
        )

        return {
            "question": req.question,
            "context": reranked
        }

    except Exception as e:
        import traceback

        return {
            "error": str(e),
            "traceback": traceback.format_exc()
        }