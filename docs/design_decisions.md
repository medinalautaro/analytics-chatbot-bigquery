# Design Decisions

## Why synthetic data

A synthetic dataset was chosen to simulate realistic e-commerce behavior while allowing full control over schema, distributions, seasonality, and data quality edge cases.

Using synthetic data also removes privacy concerns and makes the project easier to reproduce, share, and deploy without exposing sensitive business information.

---

## Why query marts instead of raw tables

The chatbot is intentionally restricted to curated dbt marts so that answers reflect tested business definitions rather than inconsistent raw event data.

Using marts also simplifies SQL generation by reducing the number of joins and transformations required at query time.

---

## Why use dbt

dbt was selected to transform raw transactional data into analytics-ready models.

This approach separates data transformation logic from application code, improves maintainability, and allows business rules to be documented and tested directly within the data platform.

---

## Why use BigQuery

BigQuery was chosen because it provides a serverless analytical database capable of handling large-scale aggregation workloads without infrastructure management.

Its native SQL support also makes it well suited for natural-language-to-SQL applications.

---

## Why use Airflow

Airflow orchestrates the end-to-end data pipeline, including data generation, validation, loading, transformation, and testing.

Using a workflow orchestrator makes the pipeline reproducible and allows failures to be detected at specific stages.

---

## Why use a hybrid chatbot architecture

Different types of user questions require different retrieval strategies.

Structured analytical questions are best answered using SQL, while documentation and business process questions are better answered using retrieval-augmented generation (RAG).

A hybrid architecture allows the system to route each request to the most appropriate component.

---

## Why use intent classification

Intent classification prevents unnecessary SQL generation for questions that are clearly informational or documentation-related.

This reduces query costs and improves response quality by selecting the correct agent before execution.

---

## Why use Retrieval-Augmented Generation (RAG)

RAG allows the chatbot to answer questions about business rules, data models, architecture decisions, and project documentation without requiring that information to be encoded directly in prompts.

This improves maintainability because documentation can evolve independently of application code.

---

## Why store documentation as Markdown

Markdown files provide a lightweight and version-controlled way to manage project knowledge.

Documentation can be updated through the same development workflow used for source code, ensuring that knowledge remains synchronized with implementation changes.

---

## Why use vector search for documentation retrieval

Vector search enables semantic retrieval of documentation even when user questions do not exactly match the wording used in the documents.

This improves the chatbot's ability to answer conceptual and exploratory questions.

---

## Why restrict SQL generation

Generated SQL is validated before execution and limited to approved datasets and tables.

This design reduces the risk of unsafe queries and prevents access to unintended data sources.

---

## Why separate retrieval and generation

The retrieval layer is responsible for finding relevant information, while the language model is responsible for generating the final response.

Separating these responsibilities makes the system easier to evaluate, debug, and improve over time.

---

## Why expose the chatbot through an API

The chatbot is implemented behind a REST API so that multiple frontends can interact with the same analytical backend.

This separation allows the user interface and analytical services to evolve independently.

---

## Why use a simple Streamlit frontend

The project focuses on demonstrating data engineering, analytics, and conversational AI capabilities rather than frontend complexity.

A lightweight Streamlit interface provides rapid development while keeping the architecture easy to understand.