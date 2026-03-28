from chatbot.core.config import settings
from chatbot.core.types import SQLResult
from chatbot.sql.matcher import match_query
from chatbot.sql.query_catalog import QUERY_CATALOG
from chatbot.sql.parameter_extractor import extract_parameters
from chatbot.sql.validator import validate_sql
from chatbot.sql.bigquery_client import BigQueryClient


class SQLExecutor:
    def __init__(self):
        self.bq = BigQueryClient(settings.google_cloud_project)

    def run(self, question: str) -> SQLResult:
        query_name = match_query(question)
        entry = QUERY_CATALOG[query_name]

        sql_template = entry["template"]

        # Protect project/dataset placeholders before Python format()
        sql_template = (
            sql_template
            .replace("{{project}}", "__PROJECT__")
            .replace("{{dataset}}", "__DATASET__")
        )

        if "parameters" in entry:
            params = extract_parameters(question, query_name)
            sql_template = sql_template.format(**params)

        sql = (
            sql_template
            .replace("__PROJECT__", settings.google_cloud_project)
            .replace("__DATASET__", settings.bigquery_dataset)
        )

        validate_sql(sql)
        rows = self.bq.query(sql)

        return SQLResult(
            query_name=query_name,
            sql=sql,
            rows=rows
        )