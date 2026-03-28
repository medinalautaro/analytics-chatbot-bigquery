from dataclasses import dataclass, field
from typing import Optional, Dict, Any


@dataclass
class ConversationState:
    last_user_question: Optional[str] = None
    last_route: Optional[str] = None
    last_query_name: Optional[str] = None
    last_sql_question: Optional[str] = None
    last_rag_question: Optional[str] = None
    last_metric: Optional[str] = None
    last_timeframe: Optional[str] = None
    last_top_k: Optional[int] = None
    last_result_summary: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)


class MemoryStore:
    def __init__(self):
        self.state = ConversationState()

    def get_state(self) -> ConversationState:
        return self.state

    def update(self, **kwargs) -> None:
        for key, value in kwargs.items():
            if hasattr(self.state, key):
                setattr(self.state, key, value)
            else:
                self.state.extra[key] = value