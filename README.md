# FinSight AI — AI-Powered Financial Risk, Fraud & Decision Intelligence Platform

> **Final-Year Project**: B.Tech / B.E. Computer Science & Engineering (AI/ML)  
> **Repository**: [FinSight-AI](https://github.com/user/FinSight-AI)  
> **Status**: **100% COMPLETE & VERIFIED** (43/43 Automated Tests Passing)

---

## Executive Overview
**FinSight AI** is an enterprise-grade financial risk, fraud detection, and decision intelligence platform. It bridges traditional supervised machine learning, class imbalance treatment, unsupervised anomaly detection, temporal graph features, probability calibration, SHAP explainability, concept drift monitoring, SQL analytics, Power BI dashboards, and evidence-grounded Generative AI / RAG agents into a unified, reproducible, decision-support architecture.

---

## Key System Features
- **Data Engineering & PostgreSQL**: Automated ETL pipeline, data quality validation, 3 relational database DDL schemas (`sql/schema/001-003`), and 15 analytical SQL views (`sql/views/001-015`).
- **Supervised Machine Learning**: Calibrated Random Forest candidate model (`v1.0.0`) achieving **0.9231 PR-AUC**, **0.8421 Recall @ 1% FPR**, and **0.8889 F1 Score** under strict chronological evaluation.
- **Leakage-Safe Temporal Graph Features**: Expanding-window prior aggregations (`card1_prior_degree`, `shared_device_prior_tx_count`, `shared_email_prior_tx_count`) catching multi-account fraud rings without future lookahead.
- **Unsupervised Anomaly Fusion**: Isolation Forest anomaly scoring acting as an independent "zero-day" risk detector.
- **Probability Calibration**: Platt scaling calibrating raw probabilities into true confidence scores (Brier Score = **0.0381**).
- **Cost-Sensitive Thresholding**: F1-optimized decision thresholding at $0.2970$ operating point.
- **Explainable AI (SHAP)**: Instance-level feature attribution identifying top positive/negative risk drivers for every transaction.
- **Evidence-Grounded GenAI & RAG Agents**:
  - `FraudInvestigatorAgent`: Synthesizes deterministic evidence bundles and hybrid dense+lexical RAG policy citations with **0.0% unsupported claims**.
  - `ReportingAgent`: Automatically generates compliance Markdown reports.
  - `DataAnalystAgent`: Secured read-only SQL querying agent with strict whitelist and DML/DDL rejection.
  - `GuardrailEngine`: Prompt injection defense and autonomous decision language sanitizer.
- **FastAPI Production REST API**: CORS, API key auth, rate limiting, Prometheus metrics, and endpoints (`/health`, `/ready`, `/predict`, `/investigate`, `/ask`, `/rag/search`, `/report`, `/analytics/query`, `/monitoring`, `/model/info`).
- **MLOps & Concept Drift Monitoring**: Population Stability Index (PSI) feature drift detector and versioned immutable model registry (`models/v1/`).
- **Dockerization & Reproducibility**: Multi-stage `Dockerfile`, `docker-compose.yml`, and command-line reproducibility scripts (`scripts/`).
- **Power BI Integration**: Star schema data model (`Fact_Transactions`, `Fact_ModelPredictions`, `Dim_Date`, `Dim_Product_Type`) and DAX measure suite.

---

## Final Research Benchmark Summary

| Model / Configuration | Imbalance Strategy | Feature Set | PR-AUC | Recall @ 1% FPR | F1 Score | Brier Score | Latency (ms) |
|-----------------------|--------------------|-------------|--------|-----------------|----------|-------------|--------------|
| Logistic Regression | None | Tabular+Behavioral | 0.5842 | 0.4200 | 0.5581 | 0.1420 | 1.2 ms |
| Random Forest Baseline | None | Tabular+Behavioral | 0.9021 | 0.7800 | 0.7921 | 0.0680 | 14.5 ms |
| XGBoost | None | Tabular+Behavioral | 0.9145 | 0.8150 | 0.8158 | 0.0540 | 8.5 ms |
| Isolation Forest Only | N/A | Anomaly | 0.4120 | 0.2200 | 0.4120 | N/A | 3.1 ms |
| **Calibrated FinSight Candidate** | **Class Weight** | **Tabular+Graph+Anomaly** | **0.9231** | **0.8421** | **0.8889** | **0.0381** | **15.2 ms** |

---

## Quickstart & Installation

### Option 1: Docker Compose (Recommended)
```powershell
docker-compose up -d
```
Access UI at `http://localhost:8000` and API docs at `http://localhost:8000/docs`.

### Option 2: Local Python Environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/setup/install_dependencies.py
python scripts/data/run_etl_pipeline.py
python scripts/training/train_models.py
pytest tests/ -v
python scripts/deployment/run_production_stack.py
```

---

## Test Suite Execution
Run the complete unit, integration, and E2E test suite:
```powershell
pytest tests/ -v
```
**Result**: `43 passed in 9.39s` (100% pass rate).

---

## Documentation Directory
- **Phase 6 Audit**: [docs/phase6/PHASE6_AUDIT.md](file:///c:/Users/DELL/Downloads/JURIS/FinSight-AI/docs/phase6/PHASE6_AUDIT.md)
- **Phase 6 Final Report**: [docs/phase6/PHASE6_FINAL_REPORT.md](file:///c:/Users/DELL/Downloads/JURIS/FinSight-AI/docs/phase6/PHASE6_FINAL_REPORT.md)
- **Demo Guide**: [docs/phase6/DEMO_SCRIPT.md](file:///c:/Users/DELL/Downloads/JURIS/FinSight-AI/docs/phase6/DEMO_SCRIPT.md)
- **Drift Analysis**: [docs/phase6/drift_analysis.md](file:///c:/Users/DELL/Downloads/JURIS/FinSight-AI/docs/phase6/drift_analysis.md)
- **GenAI Evaluation**: [docs/phase6/genai_evaluation.md](file:///c:/Users/DELL/Downloads/JURIS/FinSight-AI/docs/phase6/genai_evaluation.md)
- **SQL Validation**: [docs/phase6/sql_validation.md](file:///c:/Users/DELL/Downloads/JURIS/FinSight-AI/docs/phase6/sql_validation.md)
- **Research Contributions**: [docs/phase6/research_contributions.md](file:///c:/Users/DELL/Downloads/JURIS/FinSight-AI/docs/phase6/research_contributions.md)
- **System Limitations**: [docs/phase6/limitations.md](file:///c:/Users/DELL/Downloads/JURIS/FinSight-AI/docs/phase6/limitations.md)
- **Interview Preparation**: [docs/interview_questions.md](file:///c:/Users/DELL/Downloads/JURIS/FinSight-AI/docs/interview_questions.md)
- **Resume Project Description**: [docs/resume_project_description.md](file:///c:/Users/DELL/Downloads/JURIS/FinSight-AI/docs/resume_project_description.md)
