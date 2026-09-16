# MLOps Monitoring & Data Drift Architecture Specification — Phase 5

## 1. Overview
FinSight AI implements a dual-tier MLOps monitoring architecture:
1. **Operational Model Monitoring**: Tracks prediction volume, alert rate, risk-tier distributions, and API latency.
2. **Data Drift Monitoring**: Calculates Population Stability Index (PSI) to detect feature distribution shifts between training baseline and live inference streams.

---

## 2. Population Stability Index (PSI) Thresholds

| PSI Score Range | Classification | Action Required |
|---|---|---|
| **$\text{PSI} < 0.10$** | **NORMAL** | Distribution stable. No operational action required. |
| **$0.10 \le \text{PSI} < 0.25$** | **WARNING** | Moderate shift detected. Triggers warning log for model review. |
| **$\text{PSI} \ge 0.25$** | **DRIFT** | Significant population drift. Triggers alert for human review & retrain evaluation. |

---

## 3. Retraining Policy Workflow

```
Data / Model Drift Alert Triggered
               |
               v
     HUMAN REVIEW & AUDIT
               |
               v
     RETRAIN MODEL CANDIDATE
               |
               v
     EVALUATE & COMPARE ON HOLDOUT (PR-AUC, Brier)
               |
               v
   VALIDATE AGAINST PRODUCTION THRESHOLDS
               |
               v
   APPROVE & PROMOTE IN MODEL REGISTRY (models/v2/)
```

> [!IMPORTANT]
> **No Autonomous Retraining**:
> Models are **never** automatically redeployed into production without offline validation, leakage checks, and human sign-off.
