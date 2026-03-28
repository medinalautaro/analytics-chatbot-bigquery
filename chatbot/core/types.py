from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Any, Optional


class RouteType(str, Enum):
    SQL = "sql"
    RAG = "rag"
    HYBRID = "hybrid"


@dataclass
class SQLResult:
    query_name: str
    sql: str
    rows: List[Dict[str, Any]]