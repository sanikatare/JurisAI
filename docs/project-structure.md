# FinSight AI — Complete Repository Structure

```
FinSight-AI/
├── README.md                           # Master Project README
├── LICENSE                             # License Specification
├── .gitignore                          # Git Exclusions
├── .env.example                        # Production & Development Environment Template
├── docker-compose.yml                  # Multi-container Stack Orchestration
├── Dockerfile                          # Multi-stage Production Container Build
├── pyproject.toml                      # Package Build Configuration
├── pytest.ini                          # Test Suite Configuration
├── requirements.txt                    # Locked Python Dependencies
│
├── data/                               # Data Repository & Fixtures
│   ├── raw/                            # Raw IEEE-CIS Kaggle CSV Files (gitignored)
│   ├── interim/                        # Intermediate Cleaned DataFrames
│   ├── processed/                      # Engineered Feature DataFrames
│   ├── features/                       # Extracted Feature Matrix Maps
│   ├── sample/                         # Synthetic Test & Demo Fixtures
│   └── README.md
│
├── database/                           # PostgreSQL Schema & View Definitions
│   ├── schema/                         # DDL Schemas (001_create_tables, 002_ml, 003_monitoring)
│   ├── views/                          # 15 Analytical SQL Views (001_summary to 015_performance)
│   ├── seeds/                          # Database Fixture Seeds
│   ├── queries/                        # Analytics & Benchmark SQL Queries
│   └── README.md
│
├── src/                                # Central Production Source Code
│   ├── analytics/                      # Statistical Analytics Helpers
│   ├── anomaly/                        # Isolation Forest Anomaly Detection
│   ├── api/                            # FastAPI Production REST Endpoints & App
│   ├── data/                           # Validation, Cleaning, Extraction, Pipeline
│   ├── database/                       # SQLAlchemy / Psycopg2 Engine Connection
│   ├── features/                       # Tabular & Temporal Feature Generators
│   ├── genai/                          # Agents, Evidence Collector, Guardrails, Citations, RAG
│   ├── graph/                          # Temporal Graph Feature Extraction & GNN Gate
│   ├── ml/                             # Preprocessing, Split, Training, Calibration, Registry
│   ├── monitoring/                     # Population Stability Index (PSI) Drift Detector
│   ├── services/                       # Real-Time Prediction & Case Investigation Services
│   ├── ui/                             # Interactive Decision Support UI App
│   ├── utils/                          # Logging & Experiment Utilities
│   ├── xai/                            # TreeSHAP Feature Attribution Explainer
│   └── README.md
│
├── scripts/                            # Turnkey Automation & Reproducibility Package
│   ├── setup/                          # Environment Setup Script (install_dependencies.py)
│   ├── data/                           # ETL Pipeline Runner (run_etl_pipeline.py)
│   ├── training/                       # Model Training & Calibration (train_models.py)
│   ├── evaluation/                     # Research Experiments & Ablation Runner (run_experiments.py)
│   ├── database/                       # Database Migration & Seed Utilities
│   ├── monitoring/                     # PSI Drift Monitoring Runner
│   └── deployment/                     # Production Stack Launcher (run_production_stack.py)
│
├── experiments/                        # Experiment Outputs & Configs
│   ├── phase-03/                       # Phase 3 Baselines, Imbalance, Anomaly, Graph
│   ├── phase-04/                       # Phase 4 RAG & GenAI Experiments
│   ├── phase-05/                       # Phase 5 Latency & Monitoring Benchmarks
│   ├── phase-06/                       # Phase 6 Final Comparison, Ablation & Temporal Experiments
│   └── README.md
│
├── models/                             # Serialized Model Artifact Registry
│   ├── v1/                             # Production Model Candidate Version 1.0.0
│   ├── trained/                        # Trained Baseline Model Joblib Artifacts
│   ├── calibrated/                     # Platt Calibrator Joblib Files
│   ├── anomaly/                        # Isolation Forest Model Artifacts
│   ├── graph/                          # Graph Weights & Entity Maps
│   ├── metadata/                       # Version Metadata JSON Files
│   └── README.md
│
├── rag/                                # RAG Knowledge Base & Index Store
│   ├── documents/                      # Knowledge Base Policy SOPs (AML, Fraud, KYC, Risk)
│   ├── processed/                      # Preprocessed Text Files
│   ├── chunks/                         # Document Chunk JSON Files
│   ├── indexes/                        # Vector Store & BM25 Indexes
│   ├── metadata/                       # Chunk Metadata Maps
│   ├── evaluation/                     # Retrieval Precision/Recall Reports
│   └── README.md
│
├── powerbi/                            # Power BI Assets & Analytics Documentation
│   ├── dashboard/                      # Power BI .pbix Dashboard Asset
│   ├── datasets/                       # Star Schema Export Data
│   ├── exports/                        # Report PDF / Image Exports
│   ├── screenshots/                    # Dashboard View Screenshots
│   ├── star_schema.md                  # Relational Star Schema Specification
│   ├── dax_measures.md                 # DAX Measure Definitions
│   └── README.md
│
├── tests/                              # Categorized Test Suite (Pytest)
│   ├── unit/                           # Unit Tests (data, ml, anomaly, graph, features, monitoring, rag)
│   ├── integration/                    # Integration Tests (api, model, agents)
│   ├── security/                       # Security Tests (prompt injection, decision language)
│   ├── e2e/                            # End-to-End Smoke Test (test_full_pipeline.py)
│   └── README.md
│
├── docs/                               # Consolidated Master & Cross-Phase Documentation
│   ├── architecture/                   # Final Architecture Blueprints
│   ├── research/                       # Research Framing & Contributions
│   ├── demo/                           # Demo Guides
│   ├── presentation/                   # 19-Slide Presentation Deck
│   ├── interview_questions.md          # 30 Technical Interview Q&As
│   ├── resume_project_description.md   # Resume Material & Bullet Points
│   ├── model_card.md                   # Model Card v1.0.0
│   ├── system_card.md                  # System Guardrails Card
│   ├── limitations.md                  # Technical System Limitations
│   └── project-structure.md            # Complete Repository Tree
│
├── deployment/                         # Production Deployment Configurations
│   ├── docker/                         # Dockerfile & docker-compose.yml
│   ├── github-actions/                 # GitHub Actions CI Workflow (ci.yml)
│   ├── cloud/                          # Cloud Deployment Guide
│   └── README.md
│
├── monitoring/                         # Production Monitoring Outputs & Logs
│   ├── dashboards/                     # Real-Time Operational Monitoring Metrics
│   ├── metrics/                        # Prediction Volume & Alert Logs
│   ├── drift/                          # Population Stability Index (PSI) Logs
│   ├── logs/                           # System & Component Execution Logs
│   └── README.md
│
└── phase-wise/                         # Historical Development Phase Documentation
    ├── README.md                       # Phase Master README & Architectural Roadmap
    ├── phase-01-research/              # Research Blueprint, Problem Statement, Objectives
    ├── phase-02-data-engineering/      # ETL, Validation, Schema, Leakage Audit, Phase 2 Report
    ├── phase-03-machine-learning/      # ML Baselines, Imbalance, Anomaly, Graph, Phase 3 Report
    ├── phase-04-genai-rag/             # RAG Engine, Evidence Bundle, Agents, Phase 4 Report
    ├── phase-05-production-mlops/      # API, Docker, Model Versioning, MLOps, Phase 5 Report
    └── phase-06-final-validation/      # E2E Smoke Test, Ablation Suite, Demo, Final Report
```
