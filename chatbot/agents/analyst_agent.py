class AnalystAgent:

    def analyze(
        self,
        question: str,
        route: str,
        context: dict,
    ) -> dict:
        route_value = route.value if hasattr(route, "value") else str(route)
        return {
            "route": route,
            "reasoning": (
                
                f"Selected route '{route_value}' "
                f"for question '{question}'."
            ),
            "context": context,
        }