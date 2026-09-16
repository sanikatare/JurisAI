# FinSight AI — Phase-Wise Architecture & Project Evolution

## Master Overview
This directory documents the evolutionary development phases of **FinSight AI** ("AI-Powered Financial Risk, Fraud & Decision Intelligence Platform"). Each phase represents a complete engineering milestone in the system's progression from initial academic research to a productionized, evidence-grounded risk intelligence platform.

---

## Roadmap & Phase Progression

```
Phase 1: Research Foundation & System Blueprint
    │
    ▼
Phase 2: Data Engineering, SQL Analytics & Database Design
    │
    ▼
Phase 3: Machine Learning, Anomaly Fusion & Temporal Graph Features
    │
    ▼
Phase 4: Generative AI, RAG & Investigation Intelligence
    │
    ▼
Phase 5: Productionization, MLOps, Containerization & Drift Monitoring
    │
    ▼
Phase 6: Final System Validation, Research Experiments & Evaluation
```

---

## Summary of Phase Objectives & Key Deliverables

### [Phase 01 — Research Foundation & Blueprint](./phase-01-research/)
- **Objective**: Establish domain problem definition, research questions (RQ1–RQ7), system concept, and data leakage audit.
- **Key Deliverables**: `research-blueprint.md`, `problem-statement.md`, `research-gaps.md`, `research-questions.md`.

### [Phase 02 — Data Engineering & Database](./phase-02-data-engineering/)
- **Objective**: Data profiling, ETL pipelines, schema validation, leakage-safe chronological splits, and PostgreSQL DDL views.
- **Key Deliverables**: `001_create_tables.sql`, 15 analytical views, data validation engine (`src/data/validate.py`), `phase2-completion-report.md`.

### [Phase 03 — Machine Learning & Intelligence Layers](./phase-03-machine-learning/)
- **Objective**: Candidate Random Forest training, Isolation Forest anomaly fusion, leakage-safe graph feature extraction, Platt calibration, and TreeSHAP explainability.
- **Key Deliverables**: Candidate model `v1.0.0`, `graph_features.py`, `shap_explainer.py`, `phase3-completion-report.md`.

### [Phase 04 — GenAI, RAG & Agentic Intelligence](./phase-04-genai-rag/)
- **Objective**: Deterministic Evidence Bundle creation, Hybrid RAG Retriever (FAISS + BM25 with RRF), `FraudInvestigatorAgent`, `ReportingAgent`, `DataAnalystAgent`, and prompt/citation guardrails.
- **Key Deliverables**: `hybrid_retriever.py`, `fraud_investigator.py`, `citations.py`, `guardrails.py`, `genai-evaluation.md`.

### [Phase 05 — Productionization & MLOps](./phase-05-production-mlops/)
- **Objective**: FastAPI production endpoints, versioned Model Registry (`models/v1/`), Population Stability Index (PSI) drift detector, Docker multi-stage build, and GitHub Actions CI pipeline.
- **Key Deliverables**: `src/api/app.py`, `drift_detector.py`, `Dockerfile`, `docker-compose.yml`, `ci.yml`, `phase5-completion-report.md`.

### [Phase 06 — Final Validation & Research Evaluation](./phase-06-final-validation/)
- **Objective**: Automated 43-test suite verification, E2E smoke test, layer-by-layer ablation benchmarks, reproducible script package (`scripts/`), demo guide, presentation slides, interview prep, and final system report.
- **Key Deliverables**: `test_full_pipeline.py`, `final_results.csv`, `ablation_results.csv`, `DEMO_SCRIPT.md`, `interview_questions.md`, `phase6-final-report.md`.
