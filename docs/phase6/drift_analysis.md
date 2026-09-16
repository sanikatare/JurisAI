# FinSight AI — Temporal Drift & Population Stability Analysis (Phase 6)

## 1. Executive Summary
Financial transaction streams exhibit temporal concept drift due to shifting consumer behavior, seasonal shopping events, and evolving adversary tactics. This report evaluates the temporal stability of **FinSight AI** using a strict chronological split across three consecutive evaluation windows ($W_1, W_2, W_3$) and Population Stability Index (PSI) calculations on key feature distributions.

---

## 2. Chronological Performance Degradation

| Evaluation Window | Time Range (TransactionDT) | PR-AUC | Recall @ 1% FPR | Precision | Recall | F1 Score | Alert Volume |
|-------------------|----------------------------|--------|-----------------|-----------|--------|----------|--------------|
| **Window 1 (Baseline)** | $t_0 \to t_1$ (Months 1–2) | **0.9340** | **0.8650** | 0.9520 | 0.8570 | 0.9020 | 3.4% |
| **Window 2 (Intermediate)** | $t_1 \to t_2$ (Months 3–4) | **0.9215** | **0.8400** | 0.9380 | 0.8350 | 0.8835 | 3.8% |
| **Window 3 (Recent Holdout)** | $t_2 \to t_3$ (Months 5–6) | **0.9010** | **0.8120** | 0.9150 | 0.8010 | 0.8542 | 4.2% |

### Key Observations:
- **Performance Decay**: PR-AUC decreases by **3.53%** from Window 1 (0.9340) to Window 3 (0.9010).
- **Alert Volume Expansion**: Transaction alert volume expands from 3.4% to 4.2%, reflecting an influx of novel device signatures and user behavioral drift.
- **Why Chronological Evaluation Matters**: A random train/test split yields artificially inflated metrics (PR-AUC $\approx 0.965$) due to temporal data leakage. Chronological evaluation reflects true production generalization decay.

---

## 3. Population Stability Index (PSI) Feature Audit

| Feature Name | PSI Metric | Status | Classification | Action Triggered |
|--------------|------------|--------|----------------|------------------|
| `TransactionAmt` | 0.042 | `NORMAL` | $< 0.10$ | No action required |
| `card1_prior_degree` | 0.081 | `NORMAL` | $< 0.10$ | No action required |
| `graph_shared_device_prior_tx_count` | 0.185 | `WARNING` | $0.10 \le \text{PSI} < 0.25$ | Alert logged; queue for recalibration |
| `DeviceInfo` (New Device Encoded Ratio) | 0.268 | `DRIFT` | $\ge 0.25$ | Trigger model retraining workflow |

---

## 4. Drift Mitigation & Retraining Strategy
1. **Automated PSI Monitoring**: Daily batch evaluation via `src/monitoring/drift_detector.py`.
2. **Retraining Trigger**: If $\ge 2$ core features reach `DRIFT` status ($\text{PSI} \ge 0.25$) or PR-AUC drops below 0.880, trigger `scripts/training/train_models.py` on expanded sliding window data.
3. **Platt Recalibration**: Periodic recalibration of probability calibrator to maintain Brier score $\le 0.050$.
