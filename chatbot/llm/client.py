from openai import OpenAI
from chatbot.core.config import settings


class LLMClient:

    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)

    def generate(self, prompt: str) -> str:

        response = self.client.responses.create(
            model=settings.openai_model,
            input=prompt
        )

        return response.output_text