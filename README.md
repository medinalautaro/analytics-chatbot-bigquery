# E-commerce Analytics Chatbot with BigQuery, dbt, and Airflow

This project implements a small analytics platform designed to simulate a modern data stack. The system generates a realistic synthetic e-commerce dataset, loads it into BigQuery, and transforms the raw data into curated analytical models using dbt. Pipeline execution and data refresh are orchestrated with Apache Airflow.

On top of these analytical models, a chatbot interface allows users to query key business metrics such as revenue, customer activity, and product performance using natural language.

### Synthetic Data Validation

The dataset is validated with automated checks covering referential integrity, event ordering, and realistic behavioral patterns (long-tail purchasing and seasonal demand).