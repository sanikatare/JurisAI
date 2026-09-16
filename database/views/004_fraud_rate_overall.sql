-- View 4: Overall fraud rate (single-row KPI source)
CREATE OR REPLACE VIEW v_fraud_rate_overall AS
SELECT
    COUNT(*)                                            AS total_transactions,
    COUNT(*) FILTER (WHERE is_fraud = 1)                AS fraud_transactions,
    ROUND(100.0 * COUNT(*) FILTER (WHERE is_fraud = 1) / NULLIF(COUNT(*), 0), 4) AS fraud_rate_pct,
    ROUND((COUNT(*) - COUNT(*) FILTER (WHERE is_fraud = 1))::numeric
        / NULLIF(COUNT(*) FILTER (WHERE is_fraud = 1), 0), 2) AS imbalance_ratio_nonfraud_to_fraud
FROM fact_transactions;
