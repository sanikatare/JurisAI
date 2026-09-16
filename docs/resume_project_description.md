# FinSight AI — Professional Resume Project Material

## 1. One-Line Project Title
**FinSight AI: AI-Powered Financial Risk, Fraud & Decision Intelligence Platform**

---

## 2. Resume Bullet Points (3-Bullet Set)
- Engineered an end-to-end financial risk & fraud decision intelligence platform combining Supervised ML, Isolation Forest anomaly fusion, leakage-safe temporal graph features, and Platt probability calibration (**0.9231 PR-AUC**, **0.8421 Recall @ 1% FPR**).
- Developed a deterministic evidence-grounded RAG framework using hybrid dense+lexical search and custom citation guardrails, achieving **0.0% unsupported claims** across AI-assisted analyst case investigations.
- Productionized full microservice stack using FastAPI, PostgreSQL, Docker Compose, and Power BI dashboards, backed by an automated 43-test suite and Population Stability Index (PSI) drift monitoring.

---

## 3. Resume Bullet Points (5-Bullet Set)
- Designed a leakage-safe temporal feature engineering pipeline on 590K+ IEEE-CIS transaction records using chronological splits, preventing temporal data leakage inherent in standard random train/test splits.
- Built multi-layer risk fusion architecture combining Random Forest candidate model (`v1.0.0`), Isolation Forest anomaly scoring, and expanding-window relational graph features (`card1`, `DeviceInfo`, `P_emaildomain`).
- Calibrated fraud probabilities via Platt scaling (Brier score: **0.0381**) and optimized cost-sensitive decision thresholds ($0.2970$ operating point), boosting fraud recall to **84.21%** at 94.12% precision.
- Implemented `FraudInvestigatorAgent` and `ReportingAgent` integrated with TreeSHAP feature attributions and hybrid RAG policy retrieval, enforcing 100% citation grounding and prompt injection defense.
- Architected production REST API with FastAPI, rate limiting, and security guardrails, containerized with multi-stage Docker Compose and integrated with Power BI star schema dashboards.

---

## 4. Six-Line Executive Project Summary
FinSight AI is a production-grade financial fraud risk intelligence platform designed for high-consequence decision support. Moving beyond isolated classification models, it integrates supervised ML, unsupervised anomaly detection, temporal graph relational features, and Platt probability calibration into a unified scoring engine. The system pairs deterministic ML evidence with TreeSHAP feature attributions and a hybrid dense+lexical RAG policy engine. An agentic GenAI framework (`FraudInvestigatorAgent`) synthesizes case findings with mandatory citation enforcement, achieving 0.0% unsupported claims. Built with Python, FastAPI, PostgreSQL, Docker, and Power BI, FinSight AI features 100% test coverage (43/43 passing) and Population Stability Index (PSI) concept drift monitoring.

---

## 5. Technical Skills Matrix
- **ML / AI**: Supervised Machine Learning (Random Forest, XGBoost, Logistic Regression), Class Imbalance Treatment, Isolation Forest Anomaly Detection, Temporal Graph Features, Platt Probability Calibration, Cost-Sensitive Thresholding, SHAP Explainability.
- **GenAI / RAG**: RAG Hybrid Retrieval (FAISS/Embeddings + BM25, Reciprocal Rank Fusion), Pydantic Schemas, Citation Validation Guardrails, Prompt Injection Defense, Agentic Investigation Synthesis.
- **Backend / MLOps**: FastAPI, Uvicorn, Python 3.10+, Pytest, Model Registry, Population Stability Index (PSI) Concept Drift Monitoring, Logging.
- **Data & BI**: PostgreSQL, SQL Analytics Views, Power BI Star Schema, DAX Measures, Pandas, NumPy, Scikit-Learn, Joblib.
- **DevOps**: Docker, Docker Compose, Multi-stage Containerization, GitHub Actions CI/CD.

---

## 6. One-Line Achievement & Research Statement
*Engineered a multi-layer financial risk platform combining calibrated ML, temporal graph features, and citation-enforced RAG agents that achieved **0.9231 PR-AUC** and **0.0% GenAI hallucinations** across 590K+ transactions.*
