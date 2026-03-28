from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any


@dataclass
class HistoryItem:
    user_question: str
    resolved_question: Optional[str]
    route: Optional[str]
    query_name: Optional[str]
    sql: Optional[str]
    answer: Optional[str]


class HistoryStore:
    def __init__(self, max_items: int = 20):
        self.max_items = max_items
        self.items: List[HistoryItem] = []

    def add(
        self,
        user_question: str,
        resolved_question: Optional[str],
        route: Optional[str],
        query_name: Optional[str],
        sql: Optional[str],
        answer: Optional[str],
    ) -> None:
        self.items.append(
            HistoryItem(
                user_question=user_question,
                resolved_question=resolved_question,
                route=route,
                query_name=query_name,
                sql=sql,
                answer=answer,
            )
        )
        self.items = self.items[-self.max_items:]

    def get_history(self) -> List[Dict[str, Any]]:
        return [asdict(item) for item in self.items]