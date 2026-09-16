-- FinSight AI — Phase 5 Monitoring Database Schema
-- Creates table structures for real-time model monitoring and feature data drift tracking.

-- 1. Fact Table: Model Performance & Alert Volume Monitoring
CREATE TABLE IF NOT EXISTS fact_model_monitoring (
    monitoring_id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc'),
    model_version VARCHAR(50) NOT NULL,
    window_start TIMESTAMP WITHOUT TIME ZONE,
    window_end TIMESTAMP WITHOUT TIME ZONE,
    prediction_count INT NOT NULL,
    high_risk_count INT NOT NULL,
    medium_risk_count INT NOT NULL,
    low_risk_count INT NOT NULL,
    alert_rate NUMERIC(6, 5) NOT NULL,
    mean_calibrated_probability NUMERIC(6, 5),
    drift_status VARCHAR(20) DEFAULT 'NORMAL' CHECK (drift_status IN ('NORMAL', 'WARNING', 'DRIFT'))
);

CREATE INDEX IF NOT EXISTS idx_ml_mon_time ON fact_model_monitoring(timestamp);

-- 2. Fact Table: Feature Data Drift (PSI Tracking)
CREATE TABLE IF NOT EXISTS fact_data_drift (
    drift_id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc'),
    feature_name VARCHAR(100) NOT NULL,
    model_version VARCHAR(50) NOT NULL,
    baseline_sample_count INT NOT NULL,
    current_sample_count INT NOT NULL,
    psi_score NUMERIC(7, 5) NOT NULL,
    drift_threshold NUMERIC(5, 4) DEFAULT 0.1000,
    status VARCHAR(20) DEFAULT 'NORMAL' CHECK (status IN ('NORMAL', 'WARNING', 'DRIFT'))
);

CREATE INDEX IF NOT EXISTS idx_drift_feat ON fact_data_drift(feature_name, status);
