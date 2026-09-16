# FinSight AI — Model Registry & Serialized Artifact Store

## Overview
This directory manages serialized model artifacts, preprocessors, Platt calibrators, and versioned metadata for FinSight AI.

---

## Directory Structure
```
models/
├── v1/                       # Production Model Candidate Version 1.0.0
│   ├── model.joblib          # Trained Random Forest Candidate Model
│   ├── preprocessor.joblib   # Tabular Preprocessor (fit on train fold)
│   ├── calibrator.joblib     # Platt Probability Calibrator
│   └── metadata.json         # Immutable Version Metadata & Operating Threshold
├── trained/                  # Baseline Model Checkpoints (LR, RF, XGBoost)
├── calibrated/               # Calibration Artifacts
├── anomaly/                  # Isolation Forest Model Artifacts
├── graph/                    # Relational Graph Weights / Maps
├── metadata/                 # Model Cards & Version Records
└── README.md
```

## Runtime Code
Production model loading and inference are managed by `src/ml/registry.py` and `src/services/prediction_service.py`.
