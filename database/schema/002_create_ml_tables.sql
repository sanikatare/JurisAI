-- FinSight AI — Phase 3 Machine Learning Database Schema
-- Creates table structures for transaction model predictions and model performance metrics tracking.

-- 1. Fact Table: Machine Learning Model Predictions
-- Grain: One row per transaction per model prediction run.
CREATE TABLE IF NOT EXISTS fact_model_predictions (
    prediction_id BIGSERIAL PRIMARY KEY,
    transaction_id BIGINT NOT NULL,
    model_version VARCHAR(50) NOT NULL,
    feature_set_version VARCHAR(50) NOT NULL DEFAULT 'v1.0',
    ml_score NUMERIC(6, 5) NOT NULL, -- Calibrated probability [0.00000, 1.00000]
    predicted_label SMALLINT NOT NULL CHECK (predicted_label IN (0, 1)),
    risk_threshold NUMERIC(5, 4) NOT NULL DEFAULT 0.5000,
    anomaly_score NUMERIC(6, 5), -- Isolation forest score
    graph_risk_score NUMERIC(6, 5), -- Graph relational risk score
    evaluation_window VARCHAR(50) DEFAULT 'Holdout_Test',
    prediction_timestamp TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc')
);

CREATE INDEX IF NOT EXISTS idx_ml_pred_tx_id ON fact_model_predictions(transaction_id);
CREATE INDEX IF NOT EXISTS idx_ml_pred_model_ver ON fact_model_predictions(model_version);

-- 2. Fact Table: Machine Learning Model Performance Tracking
-- Grain: One row per model evaluation experiment run.
CREATE TABLE IF NOT EXISTS fact_model_performance (
    eval_id SERIAL PRIMARY KEY,
    model_name VARCHAR(100) NOT NULL,
    model_version VARCHAR(50) NOT NULL,
    evaluation_window VARCHAR(50) NOT NULL,
    pr_auc NUMERIC(6, 5) NOT NULL,
    recall_at_1pct_fpr NUMERIC(6, 5),
    recall_at_5pct_fpr NUMERIC(6, 5),
    precision_score NUMERIC(6, 5) NOT NULL,
    recall_score NUMERIC(6, 5) NOT NULL,
    f1_score NUMERIC(6, 5) NOT NULL,
    fpr_score NUMERIC(6, 5) NOT NULL,
    fnr_score NUMERIC(6, 5) NOT NULL,
    roc_auc NUMERIC(6, 5) NOT NULL,
    inference_latency_ms NUMERIC(8, 4),
    eval_timestamp TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc')
);

CREATE INDEX IF NOT EXISTS idx_ml_perf_model ON fact_model_performance(model_name, model_version);
