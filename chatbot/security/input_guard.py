BLOCKED_PATTERNS = [
    "ignore previous instructions",
    "ignore all previous instructions",
    "disregard previous instructions",
    "reveal your system prompt",
    "show me your system prompt",
    "drop table",
    "delete from",
    "truncate table",
    "insert into",
    "update ",
    "alter table",
]


class InputGuard:
    def __init__(self, max_length: int = 1000):
        self.max_length = max_length

    def validate(self, message: str) -> dict:
        text = (message or "").strip()

        if not text:
            return {
                "allowed": False,
                "error": "EMPTY_MESSAGE",
                "reason": "Message is empty.",
            }

        if len(text) > self.max_length:
            return {
                "allowed": False,
                "error": "MESSAGE_TOO_LONG",
                "reason": f"Message exceeds {self.max_length} characters.",
            }

        lowered = text.lower()

        for pattern in BLOCKED_PATTERNS:
            if pattern in lowered:
                return {
                    "allowed": False,
                    "error": "BLOCKED_INPUT",
                    "reason": f"Blocked unsafe input pattern: {pattern}",
                }

        return {
            "allowed": True,
            "error": None,
            "reason": None,
        }