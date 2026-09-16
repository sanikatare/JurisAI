# FinSight AI — Research Blueprint (Phase 1)

## System Vision & Goals
FinSight AI combines tabular ML, class imbalance strategies, Isolation Forest anomaly fusion, expanding-window temporal graph features, Platt probability calibration, SHAP explainability, concept drift monitoring, PostgreSQL analytics, Power BI dashboards, and evidence-grounded GenAI agents into a unified financial risk intelligence platform.

## Key Principles
1. **Deterministic Source of Truth**: All fraud scores, anomaly metrics, graph degrees, and SHAP values are computed deterministically before any LLM interaction.
2. **Zero-Hallucination GenAI**: LLM agents act strictly as decision-support tools with enforced citations (`[RAG-001]`).
3. **Leakage-Safe Temporal Ordering**: Strict chronological evaluation ($t < t_i$) eliminating optimistic random train/test split bias.
