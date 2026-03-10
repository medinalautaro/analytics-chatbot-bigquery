.PHONY: start stop build logs pipeline

start:
	cd airflow && docker compose up

stop:
	cd airflow && docker compose down

build:
	cd airflow && docker compose build

logs:
	cd airflow && docker compose logs -f

pipeline:
	echo "Trigger the pipeline from the Airflow UI:"
	echo "http://localhost:8080"