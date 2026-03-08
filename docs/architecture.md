# Architecture

## Overview
The system follows an ELT architecture:
1. Synthetic source data is generated in Python
2. Raw tables are loaded into BigQuery
3. dbt transforms raw data into curated marts
4. Airflow orchestrates the workflow
5. The chatbot queries curated marts for KPI answers

## Data layers
- raw
- staging
- intermediate
- analytics

## Chatbot strategy
The chatbot only queries approved analytics models, not raw tables, to improve reliability and business consistency.