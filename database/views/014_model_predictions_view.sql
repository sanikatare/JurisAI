-- View 014: Model Predictions Analytics View for Power BI
CREATE OR REPLACE VIEW view_model_predictions_summary AS
SELECT 
    p.prediction_id,
    p.transaction_id,
    p.model_version,
    p.ml_score,
    p.predicted_label,
    p.risk_threshold,
    p.anomaly_score,
    p.graph_risk_score,
    p.evaluation_window,
    p.prediction_timestamp,
    CASE 
        WHEN p.ml_score >= 0.80 THEN 'High Risk'
        WHEN p.ml_score >= 0.40 THEN 'Medium Risk'
        ELSE 'Low Risk'
    END AS risk_tier
FROM fact_model_predictions p;
