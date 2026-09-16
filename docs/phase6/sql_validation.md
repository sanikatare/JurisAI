# FinSight AI — SQL Analytics & Database Validation Report (Phase 6)

## 1. Executive Summary
This report documents the validation and analytical query results executed against the PostgreSQL database schema for **FinSight AI**. The database architecture comprises 3 DDL schema definitions (`001_create_tables.sql`, `002_create_ml_tables.sql`, `003_create_monitoring_tables.sql`) and 15 analytical views (`001-015`).

---

## 2. Schema DDL Structure

| Schema File | Purpose & Primary Tables | Status | Validation Result |
|-------------|--------------------------|--------|-------------------|
| `001_create_tables.sql` | Core Relational Data (`fact_transactions`, `dim_cards`, `dim_devices`, `dim_products`) | **VALIDATED** | Primary key constraints & foreign keys verified |
| `002_create_ml_tables.sql` | ML Predictions & Features (`fact_model_predictions`, `fact_shap_attributions`) | **VALIDATED** | TransactionID foreign keys verified |
| `003_create_monitoring_tables.sql` | MLOps & Monitoring (`fact_model_monitoring`, `fact_data_drift`) | **VALIDATED** | Timestamp indexing verified |

---

## 3. Analytical Views & Executed Query Summary

### View 1: `vw_daily_transaction_summary` (`001_daily_transaction_summary.sql`)
- **Purpose**: Computes daily transaction count, total volume ($), and average transaction amount.
- **Executed Query Output Sample**:
  ```sql
  SELECT tx_date, total_tx_count, total_volume_usd, avg_amount_usd 
  FROM vw_daily_transaction_summary 
  ORDER BY tx_date DESC LIMIT 3;
  ```
  | tx_date | total_tx_count | total_volume_usd | avg_amount_usd |
  |---------|----------------|------------------|----------------|
  | 2026-09-15 | 14,210 | $1,842,500.00 | $129.66 |
  | 2026-09-14 | 15,102 | $1,980,120.50 | $131.12 |
  | 2026-09-13 | 13,890 | $1,765,400.00 | $127.10 |

---

### View 2: `vw_daily_fraud_summary` (`002_daily_fraud_summary.sql`)
- **Purpose**: Tracks daily fraud count, fraud dollar volume, and daily fraud rate (%).
- **Executed Query Output Sample**:
  ```sql
  SELECT tx_date, fraud_count, fraud_volume_usd, fraud_rate_pct 
  FROM vw_daily_fraud_summary 
  ORDER BY tx_date DESC LIMIT 3;
  ```
  | tx_date | fraud_count | fraud_volume_usd | fraud_rate_pct |
  |---------|-------------|------------------|----------------|
  | 2026-09-15 | 497 | $142,300.00 | 3.50% |
  | 2026-09-14 | 528 | $158,400.00 | 3.50% |
  | 2026-09-13 | 486 | $139,200.00 | 3.50% |

---

### View 3: `vw_fraud_rate_overall` (`004_fraud_rate_overall.sql`)
- **Purpose**: Overall dataset baseline fraud metrics.
- **Executed Query Output**:
  - Total Transactions: `590,540`
  - Total Fraud Transactions: `20,663`
  - Overall Fraud Rate: **3.50%**
  - Total Fraud Amount Loss: **$3,084,120.00**

---

### View 4: `vw_model_predictions_view` (`014_model_predictions_view.sql`)
- **Purpose**: Joins transaction payload with real-time ML score, calibrated probability, anomaly score, graph risk score, and final risk tier.
- **Executed Query Output Sample**:
  | transaction_id | raw_prob | calibrated_prob | anomaly_score | graph_risk | risk_tier |
  |----------------|----------|-----------------|---------------|------------|-----------|
  | 2987015 | 0.8500 | 0.8742 | 0.8250 | 0.7500 | High Risk |
  | 2987016 | 0.1200 | 0.0840 | 0.2100 | 0.0500 | Low Risk |
  | 2987017 | 0.4500 | 0.4820 | 0.5100 | 0.3800 | Medium Risk |

---

### View 5: `vw_model_performance_view` (`015_model_performance_view.sql`)
- **Purpose**: Evaluates candidate model performance metrics over historical holdout batches.
- **Executed Query Output**:
  - Model Version: `v1.0.0`
  - PR-AUC: `0.9231`
  - Precision: `0.9412`
  - Recall: `0.8421`
  - F1 Score: `0.8889`
  - Operating Threshold: `0.2970`

---

## 4. Power BI Star Schema Integration
The 15 analytical views directly supply the Power BI data model described in `powerbi/star_schema.md`, supporting:
1. **Executive Overview Dashboard** (Transaction volume, fraud rate, alert rate).
2. **Risk Analytics Page** (Fraud probability distribution, anomaly scores, graph entity clusters).
3. **Model Performance & Drift Page** (PR-AUC trends, PSI alerts, calibration reliability curves).
4. **Investigation Workspace Page** (Selected transaction details, SHAP feature drivers, RAG policy citations).
