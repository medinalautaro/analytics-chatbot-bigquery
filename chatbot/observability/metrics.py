import time


class RequestMetrics:
    def __init__(self):
        self.start_time = time.perf_counter()

    def finish(self) -> dict:
        return {
            "response_time_ms": round(
                (time.perf_counter() - self.start_time) * 1000,
                2
            )
        }