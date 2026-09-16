-- View 015: Model Performance Monitoring View for Power BI
CREATE OR REPLACE VIEW view_model_performance_summary AS
SELECT 
    eval_id,
    model_name,
    model_version,
    evaluation_window,
    pr_auc,
    recall_at_1pct_fpr,
    recall_at_5pct_fpr,
    precision_score,
    recall_score,
    f1_score,
    fpr_score,
    fnr_score,
    roc_auc,
    inference_latency_ms,
    eval_timestamp
FROM fact_model_performance
ORDER BY eval_timestamp DESC;
