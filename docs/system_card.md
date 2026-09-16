# System Card — FinSight AI Financial Risk Intelligence Platform

## System Overview
FinSight AI is an production-oriented, AI-powered financial risk, fraud detection, and decision intelligence platform. It integrates scalable data engineering, PostgreSQL analytics, supervised machine learning, unsupervised anomaly detection, temporal entity graph features, explainable AI (SHAP), hybrid Retrieval-Augmented Generation (RAG), and grounded Generative AI decision support.

> [!IMPORTANT]
> **Academic & Research Disclosure**:
> FinSight AI is a final-year academic research project and portfolio artifact. It is trained on public Kaggle IEEE-CIS competition data and representative SOP policy documents. It is **not** an operational banking enforcement system and must not be used to autonomously block accounts or freeze funds without human review.

---

## Technical Stack & Architectural Layers
- **Data Engineering & Storage**: Python ETL, PostgreSQL 15, SQL Views (001-015), Star Schema.
- **Machine Learning Layer**: Scikit-Learn Random Forest Candidate (`v1.0.0`), Class Weighting, Platt Probability Calibration, 100-step Threshold Sweep.
- **Advanced Feature Intelligence**: Unsupervised Isolation Forest Anomaly Detection, Temporal Graph Relational Features (`card1`, normalized `DeviceInfo`).
- **Explainability**: SHAP (SHapley Additive exPlanations) Top-3 feature drivers (`[SHAP-001]`).
- **GenAI & RAG Decision Support**: Fast hybrid dense (FAISS) + lexical (BM25) RAG, Evidence Bundle Collector, Fraud Investigator Agent, Reporting Agent, Read-Only SQL Analyst Agent, Output Guardrails.
- **MLOps & API**: FastAPI, Docker, Docker Compose, Pytest Pyramid (38+ tests), PSI Drift Monitoring.

---

## Intended Use & Safety Controls
- **Intended Use**: Financial risk analyst decision support, fraud pattern exploration, interactive case investigation, automated report compilation.
- **Safety Safeguards**: Input prompt injection detection, output decision language filter (neutralizing "freeze card" into "elevated risk warranting review"), strict read-only SQL AST verification.
