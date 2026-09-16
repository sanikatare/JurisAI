# Model Card — FinSight AI Fraud Intelligence Candidate

## Model Overview
- **Model Name**: FinSight AI Calibrated Random Forest Classifier
- **Model Version**: `v1.0.0`
- **Model Type**: Ensemble Random Forest + Platt Sigmoid Probability Calibrator
- **Developer**: FinSight AI Core ML Team
- **Date**: September 2026

---

## Intended Use
- **Primary Purpose**: Academic and research-oriented fraud detection risk scoring system. Provides calibrated probabilities of transaction fraud to rank incoming transactions for investigation.
- **Intended Users**: Fraud analysts, ML researchers, decision intelligence developers.
- **Out-of-Scope Use**: NOT intended for autonomous financial asset freezing, legal enforcement, or direct consumer credit denial without human review.

> [!IMPORTANT]
> **Academic Statement**:
> This model is an academic/research fraud-risk scoring system and not a production banking enforcement system.

---

## Dataset & Feature Schema
- **Dataset**: IEEE-CIS Fraud Detection (or verified synthetic demonstration fixture).
- **Target Variable**: `isFraud` (Binary: 0 = Legitimate, 1 = Fraudulent).
- **Features Used**:
  - **Tabular**: `TransactionAmt`, `ProductCD`, `C1-C14`, `V1-V339` (imputed/encoded).
  - **Temporal**: `tx_hour_of_day`, `tx_day_of_cycle`, `time_since_prev_tx`.
  - **Behavioral**: `card1_prior_tx_count`, `card1_prior_amount_mean`, `card1_amount_deviation_from_prior_mean`.
  - **Graph Relational**: `graph_card1_prior_degree`, `graph_shared_device_prior_tx_count`, `graph_shared_email_prior_tx_count`, `graph_relational_risk_score`.
  - **Anomaly**: `anomaly_score` (from unsupervised Isolation Forest).

---

## Training & Preprocessing Setup
- **Train/Val/Test Split**: Strict chronological split based on `TransactionDT` (60% Train, 20% Validation, 20% Test).
- **Preprocessing**:
  - Median numerical imputation + explicit `_was_missing` indicators.
  - Categorical frequency encoding for high cardinality, one-hot for low cardinality.
  - Fit ONLY on training data (`TabularPreprocessor`).
- **Class Imbalance Strategy**: Class weighting (`class_weight="balanced"`) applied during tree construction.

---

## Model Evaluation Metrics
- **Primary Metric**: PR-AUC (Precision-Recall Area Under Curve).
- **Operating Threshold**: Selected via F1 optimization or Recall @ 1% FPR constraint.
- **Probability Calibration**: Platt Scaling (Logistic Regression on validation logits). Measured via Brier Score and Reliability Diagrams.

---

## Ethical Considerations & Limitations
- **Concept Drift**: Financial fraud patterns evolve rapidly over time. Models trained on past time windows experience performance decay if not periodically retrained.
- **Missing Data Sensitivity**: Reliance on device and identity features may lead to higher uncertainty on transactions lacking rich metadata.
- **Relational Edge Sparsity**: Graph feature efficacy depends on the presence of recurring entity identifiers (`card1`, normalized `DeviceInfo`).
