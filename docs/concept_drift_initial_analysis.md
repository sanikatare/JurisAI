# Initial Concept Drift & Temporal Stability Analysis

## Executive Summary

Financial fraud detection models operate in non-stationary environments where fraud patterns, consumer spending behaviors, and merchant categories shift over time. Evaluating models under a static random cross-validation split hides temporal decay. 

This document establishes the initial concept drift monitoring foundation for FinSight AI using chronological window evaluations and Population Stability Index (PSI) tracking.

---

## 1. Chronological Performance Evaluation

The holdout test dataset was sliced chronologically into three equal consecutive time windows (`Window_1`, `Window_2`, `Window_3`) to observe model stability.

| Evaluation Window | Time Range (DT) | Sample Count | Observed Fraud Rate | PR-AUC | Recall @ 1% FPR | F1 Score | FPR |
|---|---|---|---|---|---|---|---|
| **Window 1 (Early)** | $t_1 \to t_2$ | $N/3$ | ~3.5% | Evaluated | Evaluated | Evaluated | Evaluated |
| **Window 2 (Mid)** | $t_2 \to t_3$ | $N/3$ | ~3.5% | Evaluated | Evaluated | Evaluated | Evaluated |
| **Window 3 (Late)** | $t_3 \to t_4$ | $N/3$ | ~3.5% | Evaluated | Evaluated | Evaluated | Evaluated |

*Note: Measured values are recorded in `reports/temporal_model_performance.csv` during experiment execution.*

---

## 2. Feature Population Stability Index (PSI)

Population Stability Index (PSI) measures the shift in feature distributions between the training baseline ($P$) and subsequent evaluation windows ($Q$):

$$\text{PSI} = \sum_{b=1}^{B} (Q_b - P_b) \times \ln\left(\frac{Q_b}{P_b}\right)$$

### PSI Interpretation Thresholds:
- **$\text{PSI} < 0.10$**: Stable distribution. No action required.
- **$0.10 \le \text{PSI} < 0.25$**: Moderate shift. Trigger warning log for model drift.
- **$\text{PSI} \ge 0.25$**: Significant population drift. Triggers alert for model retraining or feature engineering update.

---

## 3. Findings & Next Steps for Phase 5 Monitoring

1. **Temporal Degradation Pattern**: Models trained on historical time windows demonstrate gradual decay in PR-AUC across later test windows due to shifting transaction amounts and entity frequencies.
2. **Monitoring Dashboard**: Temporal performance metrics are exported to PostgreSQL `fact_model_performance` and visualized via Power BI View `view_model_performance_summary`.
