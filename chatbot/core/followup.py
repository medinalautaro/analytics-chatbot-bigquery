import re
from chatbot.core.memory import ConversationState


FOLLOWUP_PATTERNS = {
    "previous_month": [
        "previous month",
        "month before",
        "prior month",
    ],
    "there_reference": [
        "there",
        "that one",
        "that period",
        "that month",
    ],
}


def is_followup_question(question: str) -> bool:
    q = question.lower().strip()

    followup_markers = [
        "what about",
        "there",
        "that one",
        "that metric",
        "that period",
        "prior month",
        "same metric",
        "same period",
    ]

    return any(marker in q for marker in followup_markers)


def resolve_followup(question: str, state: ConversationState) -> str:
    q = question.lower().strip()

    if not state.last_user_question:
        return question

    # "what about the previous month?"
    if any(p in q for p in FOLLOWUP_PATTERNS["previous_month"]):
        if state.last_metric == "revenue":
            return "revenue previous month"
        if state.last_metric == "orders":
            return "orders previous month"
        if state.last_metric == "avg_order_value":
            return "average order value previous month"
        if state.last_metric == "top_channels":
            top_k = state.last_top_k or 3
            return f"top {top_k} channels previous month"

    # "top 3 channels there"
    top_channels_match = re.search(r"\btop\s+(\d+)\s+channels?\b", q)
    if top_channels_match:
        top_k = int(top_channels_match.group(1))

        if any(p in q for p in FOLLOWUP_PATTERNS["there_reference"]):
            if state.last_timeframe:
                return f"top {top_k} channels {state.last_timeframe}"

        if "month" not in q and state.last_timeframe:
            return f"top {top_k} channels {state.last_timeframe}"

    # "what does that metric mean?"
    if "that metric" in q or "what does that mean" in q:
        if state.last_metric:
            if state.last_metric == "avg_order_value":
                return "what does avg_order_value mean?"
            if state.last_metric == "top_channels":
                return "what does revenue mean?"
            return f"what does {state.last_metric} mean?"

    # "there" / "that period"
    if any(p in q for p in FOLLOWUP_PATTERNS["there_reference"]):
        if state.last_metric and state.last_timeframe:
            if state.last_metric == "revenue":
                return f"revenue {state.last_timeframe}"
            if state.last_metric == "orders":
                return f"orders {state.last_timeframe}"
            if state.last_metric == "avg_order_value":
                return f"average order value {state.last_timeframe}"
            if state.last_metric == "top_channels":
                top_k = state.last_top_k or 3
                return f"top {top_k} channels {state.last_timeframe}"

    # bare "and top 3 channels"
    if q.startswith("and ") and state.last_timeframe:
        stripped = question[4:].strip()
        top_channels_match = re.search(r"\btop\s+(\d+)\s+channels?\b", stripped.lower())
        if top_channels_match:
            top_k = int(top_channels_match.group(1))
            return f"top {top_k} channels {state.last_timeframe}"
        return f"{stripped} {state.last_timeframe}"

    return question