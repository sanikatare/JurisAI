# FinSight AI — Machine Learning Data Leakage Audit (Phase 3)

## 1. Executive Summary

Data leakage occurs when information from outside the training dataset (or from future timestamps, target-adjacent aggregations, or test sets) is inadvertently used to create features or fit model parameters. In financial fraud detection, data leakage causes artificially inflated evaluation metrics (e.g. fake 0.99 PR-AUC) that immediately fail in production environments.

This 10-point audit explicitly inspects, documents, and enforces safeguards across the Phase 3 ML pipeline.

---

## 2. 10-Point Leakage Verification Audit

| Audit Category | Potential Leakage Mechanism | Risk Level | Mitigation & Technical Implementation | Verification Method |
|---|---|---|---|---|
| **1. Target Leakage** | Target column `isFraud` included in feature matrix or used in feature encoding | **Critical** | Target column explicitly excluded from `feature_cols` in `src/ml/experiment_runner.py`. Unsupervised models (Isolation Forest) fit strictly without `y`. | Code audit + `test_anomaly_unsupervised.py` |
| **2. Future Information** | Features using transactions occurring after row $i$'s timestamp $t_i$ | **Critical** | Chronological ordering enforced via `TransactionDT`. Features derived strictly using `.shift(1)` expanding windows. | Unit test (`test_time_since_previous_transaction_never_uses_future_rows`) |
| **3. Post-Transaction Info** | Features collected after a fraud investigation is triggered (e.g. manual review comments) | **High** | IEEE-CIS columns audited; post-transaction review columns excluded from feature set. | Feature schema inspection |
| **4. Identifier Leakage** | Raw unique primary keys (`TransactionID`) fed into model, causing overfitting | **High** | Primary key dropped from feature matrix prior to model training. | Schema validation |
| **5. Duplicate Leakage** | Exact duplicate rows split across training and test sets | **Medium** | Deduplication check executed during Phase 2 ETL (`src/data/clean.py`); chronological split eliminates random cross-contamination. | `test_duplicate_rows_are_flagged_not_silently_dropped` |
| **6. Train/Test Overlap** | Random splitting causing temporal overlap or identity lookup across splits | **High** | Strict chronological split (`train_max_time < val_min_time < test_min_time`) enforced in `src/ml/split.py`. | `test_ml_split.py` |
| **7. Preprocessor Leakage** | Imputer medians, scalers, or encoders fit on entire dataset (train + val + test) | **High** | `TabularPreprocessor` is fit ONLY on `X_train`. `.transform()` applied separately to validation/test folds. | `test_ml_preprocessing.py` |
| **8. SMOTE Leakage** | Oversampling applied before splitting, generating synthetic test neighbors | **Critical** | SMOTE executed exclusively within `imblearn.pipeline.Pipeline` on training data. Validation and test sets remain untouched. | `test_ml_smote_leakage.py` |
| **9. Feature-Engineering Leakage** | Rolling entity statistics including current transaction amount in expanding mean | **High** | All entity expanding aggregations use `.shift(1)` before cumulative calculation (`src/features/entity_features.py`). | `test_entity_rolling_amount_mean_excludes_current_row` |
| **10. Calibration Leakage** | Probability calibrator (Platt / Isotonic) fit on test set or training set | **Medium** | Calibrator fit strictly on validation probabilities (`y_val_prob`) and evaluated on held-out test data (`y_test`). | `test_metrics_and_calibration.py` |

---

## 3. Audit Conclusion & Approval

The Phase 3 Machine Learning pipeline has passed all 10 leakage verification checkpoints. All preprocessing, scaling, resampling, graph feature extraction, and probability calibration steps maintain strict temporal ordering and split isolation.
