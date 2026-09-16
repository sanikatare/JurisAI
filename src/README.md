# FinSight AI — Central Production Source Code (`src/`)

## Overview
This directory contains the central production Python packages and application source code for **FinSight AI**.

---

## Package Organization

```
src/
├── analytics/         # Statistical Analytics & Summary Helpers
├── anomaly/           # Isolation Forest Unsupervised Anomaly Detection
├── api/               # FastAPI Production REST Endpoints & Routes (`app.py`, `routes/`)
├── data/              # Validation, Cleaning, Extraction, Pipeline (`clean.py`, `validate.py`)
├── database/          # SQLAlchemy / Psycopg2 PostgreSQL Database Connection Engine
├── features/          # Tabular & Temporal Feature Engineering (`entity_features.py`)
├── genai/             # GenAI Agents (`fraud_investigator.py`), Evidence Collector, Guardrails, RAG
├── graph/             # Temporal Graph Feature Extraction & GNN Decision Gate (`graph_features.py`)
├── ml/                # Preprocessor, Split, Baseline Models, Platt Calibrator, Threshold, Registry
├── monitoring/        # Population Stability Index (PSI) Drift Detector & Log Monitor
├── services/          # Real-Time Prediction & Case Investigation Orchestration Services
├── ui/                # Interactive Decision Support Workspace Web UI (`app.py`)
├── utils/             # JSON Logging Configuration & Synthetic Experiment Runner
└── xai/               # TreeSHAP Feature Attribution Explainer (`shap_explainer.py`)
```
