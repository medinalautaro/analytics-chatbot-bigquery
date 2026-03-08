from pathlib import Path
import pandas as pd
from google.cloud import bigquery

PROJECT_ID = "project-f3e4931e-2406-418c-917"
DATASET_ID = "raw"
DATA_DIR = Path("data/generated")

TABLE_FILES = {
    "customers": "customers.csv",
    "products": "products.csv",
    "orders": "orders.csv",
    "order_items": "order_items.csv",
    "payments": "payments.csv",
    "shipments": "shipments.csv",
    "returns": "returns.csv",
    "marketing_spend": "marketing_spend.csv",
}

DATE_COLUMNS = {
    "customers": ["signup_date"],
    "orders": ["order_timestamp"],
    "payments": ["payment_timestamp"],
    "shipments": ["shipment_timestamp", "delivery_timestamp"],
    "returns": ["return_timestamp"],
    "marketing_spend": ["date"],
}


def main() -> None:
    client = bigquery.Client(project=PROJECT_ID)

    for table_name, filename in TABLE_FILES.items():
        file_path = DATA_DIR / filename
        print(f"Loading {file_path} -> {PROJECT_ID}.{DATASET_ID}.{table_name}")

        parse_dates = DATE_COLUMNS.get(table_name, [])
        df = pd.read_csv(file_path, parse_dates=parse_dates)

        table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"

        job_config = bigquery.LoadJobConfig(
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
            autodetect=True,
        )

        job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
        job.result()

        table = client.get_table(table_id)
        print(f"Loaded {table.num_rows:,} rows into {table_id}")


if __name__ == "__main__":
    main()