# FinSight AI — Research Experiments Directory

## Overview
This directory organizes all research experiment configurations, outputs, and metrics generated across the development lifecycle of FinSight AI.

---

## Structure
```
experiments/
├── phase-03/
│   ├── exp-01-baselines/     # Supervised baselines (LR, RF, XGBoost)
│   ├── exp-02-imbalance/     # Class imbalance (None vs Class Weighting vs SMOTE)
│   ├── exp-03-anomaly/       # Isolation Forest anomaly score fusion
│   ├── exp-04-graph/         # Relational graph feature extraction
│   ├── exp-05-gnn/           # GNN Go/No-Go evaluation
│   ├── exp-06-xai/           # SHAP feature attributions
│   └── exp-07-drift/         # Initial temporal concept drift analysis
├── phase-04/
│   ├── rag/                  # RAG hybrid retriever evaluation
│   └── genai/                # GenAI agent grounding benchmark
├── phase-05/
│   ├── latency/              # Production API latency benchmarks
│   └── monitoring/           # Population Stability Index (PSI) drift logs
└── phase-06/
    ├── final-comparison/     # Master model comparison matrix
    ├── ablation/             # 7-layer intelligence ablation suite
    └── drift/                # 6-month chronological holdout evaluation
```
