import json
from pathlib import Path


SUMMARY_PATH = Path("evaluation/eval_summary.json")
REPORT_PATH = Path("evaluation/eval_report.md")


def main():
    summary = json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))

    report = f"""# Evaluation Report

## Model Performance

| Metric | Value |
|---|---:|
| Average latency ms | {summary.get("avg_latency_ms")} |
| Average reported response time ms | {summary.get("avg_reported_response_time_ms")} |
| Average estimated tokens | {summary.get("avg_total_tokens_est")} |
| Average semantic similarity | {summary.get("avg_semantic_similarity")} |

## Agent Performance

| Metric | Value |
|---|---:|
| Route accuracy | {summary.get("route_accuracy")} |
| Agent decision coherence | {summary.get("agent_decision_coherence")} |
| Agent dialogue completeness | {summary.get("agent_dialogue_completeness")} |
| Agent redundancy avoidance | {summary.get("agent_redundancy_avoidance")} |
| Average agent steps | {summary.get("avg_agent_steps")} |

## RAG Efficiency

| Metric | Value |
|---|---:|
| RAG context coverage | {summary.get("rag_context_coverage")} |
| RAG recall proxy | {summary.get("rag_recall_proxy")} |
| RAG precision@k | {summary.get("rag_precision_at_k")} |
| Average RAG sources | {summary.get("avg_rag_sources")} |
| Average RAG retrieval time ms | {summary.get("avg_rag_retrieval_time_ms")} |

## Security and Robustness

| Metric | Value |
|---|---:|
| Blocked cases | {summary.get("blocked_cases")} |
| SQL cases with rows | {summary.get("sql_cases_with_rows")} |
| RAG cases with sources | {summary.get("rag_cases_with_sources")} |
"""

    REPORT_PATH.write_text(report, encoding="utf-8")
    print(f"Saved {REPORT_PATH}")


if __name__ == "__main__":
    main()