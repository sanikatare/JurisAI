# Model Versioning & Lightweight Registry Specification

## 1. Overview
Model versioning ensures that every ML prediction and risk assessment served by FinSight AI is fully auditable, reproducible, and traceable back to exact model artifacts, feature schemas, training datasets, and hyperparameters.

---

## 2. Directory Structure & Version Schema

```
models/
└── v1/
    ├── model.joblib              # Serialized candidate Random Forest classifier
    ├── preprocessor.joblib       # Fitted TabularPreprocessor pipeline
    ├── calibrator.joblib         # Fitted Platt Sigmoid calibrator
    └── metadata.json             # Immutable model version metadata contract
```

---

## 3. Registered Version Metadata Contract (`metadata.json`)

```json
{
  "model_id": "MOD-RF-2026-V1",
  "model_name": "Calibrated_Random_Forest",
  "version": "v1.0.0",
  "status": "production",
  "training_date": "2026-09-17",
  "dataset_version": "IEEE-CIS-Phase3",
  "metrics": {
    "pr_auc": 0.9231,
    "recall_at_1pct_fpr": 0.8421,
    "f1_score": 0.8889,
    "roc_auc": 0.9750,
    "brier_score": 0.02047
  },
  "threshold": 0.2970,
  "calibration_method": "Platt Scaling (Sigmoid)",
  "artifact_files": [
    "model.joblib",
    "preprocessor.joblib",
    "calibrator.joblib"
  ]
}
```

---

## 4. Promotion Lifecycle
Model versions follow a strict 5-stage promotion lifecycle:
1. `development`: Experimental prototype undergoing offline evaluation.
2. `candidate`: Trained model submitted for validation checks.
3. `validated`: Passed leakage audit, threshold analysis, and calibration checks.
4. `production`: Currently deployed in the active prediction service endpoint (`/api/v1/predict`).
5. `retired`: Archived model version replaced by a superior validated candidate.
