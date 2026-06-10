# Business Rules

## Data Governance

### BR-001: Read-Only Access
The chatbot must never execute INSERT, UPDATE, DELETE, DROP, TRUNCATE, ALTER, or CREATE statements against analytical datasets.

**Reason:** Prevent accidental modification of production data.

---

### BR-002: Approved Dataset Access
Queries can only be executed against datasets explicitly configured in the application settings.

**Reason:** Prevent access to unauthorized data sources.

---

### BR-003: No Cross-Project Queries
Users cannot execute queries against external Google Cloud projects.

**Reason:** Enforce organizational data boundaries.

---

## Query Validation

### BR-004: Query Cost Protection
Queries estimated to scan more than a configurable threshold (e.g., 5 GB) must be rejected or require confirmation.

**Reason:** Control BigQuery costs.

---

### BR-005: Result Size Limitation
Query results returned to the user must be limited to a maximum number of rows (default: 100).

**Reason:** Prevent excessive data transfer and improve response times.

---

### BR-006: SQL Safety Check
Every generated SQL statement must pass validation before execution.

Validation includes:

- Allowed datasets only
- No DDL statements
- No DML statements
- No scripting statements

**Reason:** Protect data integrity.

---

## Analytics Rules

### BR-007: Revenue Calculation
Revenue is defined as:

Revenue = SUM(quantity × unit_price)

Refunded orders must be excluded unless explicitly requested.

---

### BR-008: Customer Count
A customer is considered active if at least one order exists during the selected period.

---

### BR-009: Average Order Value
Average Order Value (AOV) is calculated as:

AOV = Total Revenue / Number of Orders

Cancelled orders are excluded.

---

### BR-010: Top Products Ranking
Product rankings must be based on revenue by default.

Alternative ranking metrics (quantity sold, order count) require explicit user request.

---

## RAG Rules

### BR-011: Source Attribution
Every answer generated using retrieved documents must include the originating document source.

**Reason:** Improve explainability.

---

### BR-012: Minimum Context Confidence
If retrieved context relevance falls below the configured threshold, the chatbot must respond that insufficient information was found.

**Reason:** Reduce hallucinations.

---

### BR-013: Documentation Priority
When both structured data and documentation are available, documentation is used only for explanatory content, not numerical metrics.

**Reason:** Ensure numerical accuracy.

---

## Conversational Rules

### BR-014: Clarification Requirement
If the user's request is ambiguous, the chatbot must ask for clarification before generating SQL.

Example:

- "Show me sales"
- "Show me customer performance"

---

### BR-015: Time Period Default
When no date range is provided:

- Revenue metrics default to the last 30 days.
- Operational metrics default to the current month.

---

### BR-016: Follow-Up Context
The chatbot may use conversation history to resolve follow-up questions, but only within the active session.

---

## Data Quality Rules

### BR-017: Null Revenue Values
Null revenue values must be treated as zero during aggregations.

---

### BR-018: Duplicate Orders
Duplicate order IDs must be excluded from analytical calculations.

---

### BR-019: Future Dates
Transactions with dates greater than the current date must be flagged as data quality issues and excluded from reports.

---

## Monitoring Rules

### BR-020: Query Logging
Every executed query must be logged with:

- Timestamp
- User request
- Generated SQL
- Execution time
- Rows returned

---

### BR-021: Failed Query Tracking
All failed SQL executions must be stored for future analysis and prompt improvement.

---

### BR-022: RAG Retrieval Metrics
The system must record:

- Retrieved documents
- Retrieval latency
- Relevance scores

for every RAG interaction.
