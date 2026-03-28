from typing import List, Optional, Literal
from pydantic import BaseModel, Field


RouteType = Literal["sql", "rag", "hybrid", "unknown"]


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class SourceItem(BaseModel):
    title: str
    snippet: str


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    history: List[ChatMessage] = []


class ChatResponse(BaseModel):
    answer: str
    route: RouteType = "unknown"
    sql: Optional[str] = None
    sources: List[SourceItem] = []
    history: List[ChatMessage] = []
    error: Optional[str] = None