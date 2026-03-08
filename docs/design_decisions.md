# Design Decisions

## Why synthetic data
A synthetic dataset was chosen to simulate realistic e-commerce behavior while allowing full control over schema, distributions, seasonality, and data quality edge cases.

## Why query marts instead of raw tables
The chatbot is intentionally restricted to curated dbt marts so that answers reflect tested business definitions rather than inconsistent raw event data.