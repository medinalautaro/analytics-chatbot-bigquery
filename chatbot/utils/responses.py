from chatbot.schemas import ChatResponse, ChatMessage, SourceItem


def success_response(
    answer: str,
    route: str = "unknown",
    sql: str | None = None,
    sources: list[SourceItem] | None = None,
    history: list[ChatMessage] | None = None,
) -> ChatResponse:
    return ChatResponse(
        answer=answer,
        route=route,
        sql=sql,
        sources=sources or [],
        history=history or [],
        error=None,
    )


def error_response(
    answer: str,
    error: str,
    route: str = "unknown",
    sql: str | None = None,
    sources: list[SourceItem] | None = None,
    history: list[ChatMessage] | None = None,
) -> ChatResponse:
    return ChatResponse(
        answer=answer,
        route=route,
        sql=sql,
        sources=sources or [],
        history=history or [],
        error=error,
    )