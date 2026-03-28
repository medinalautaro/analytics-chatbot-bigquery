from google.cloud import bigquery


class BigQueryClient:

    def __init__(self, project_id: str):
        self.client = bigquery.Client(project=project_id)

    def query(self, sql: str):
        job = self.client.query(sql)
        rows = job.result()
        return [dict(row) for row in rows]