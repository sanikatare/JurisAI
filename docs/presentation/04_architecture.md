# Slide 4: System Architecture

## End-to-End Pipeline Blueprint
```
Data Ingestion -> Schema Validation -> Preprocessing -> Candidate Model (v1.0.0)
 -> Anomaly Fusion -> Graph Features -> Platt Calibration -> SHAP Explainability
 -> Evidence Bundle -> Hybrid RAG Policy Search -> GenAI Investigation
 -> FastAPI -> React/HTML Web UI -> PostgreSQL / Monitoring -> Power BI
```
- **Source of Truth**: Deterministic ML/risk engines computed before any LLM interaction.
- **Decision Support**: LLM acts strictly as an analyst assistant, barred from autonomous enforcement actions.
