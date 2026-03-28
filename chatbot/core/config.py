import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    google_cloud_project: str = os.getenv("GOOGLE_CLOUD_PROJECT", "")
    bigquery_dataset: str = os.getenv("BIGQUERY_DATASET", "")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    def validate(self):
            missing = []

            if not self.openai_api_key:
                missing.append("openai_api_key")
            if not self.google_cloud_project:
                missing.append("google_cloud_project")
            if not self.bigquery_dataset:
                missing.append("bigquery_dataset")

            if missing:
                raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

settings = Settings()