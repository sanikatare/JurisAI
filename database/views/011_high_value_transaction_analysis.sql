-- View 11: High-value transaction analysis
-- Threshold uses the measured p95 amount (from v_transaction_amount_statistics)
-- rather than an arbitrary hardcoded dollar figure, since "high value" is
-- dataset-relative and Vesta anonymized/rescaled TransactionAmt.
CREATE OR REPLACE VIEW v_high_value_transaction_analysis AS
WITH threshold AS (
    SELECT percentile_cont(0.95) WITHIN GROUP (ORDER BY transaction_amt) AS p95_amount
    FROM fact_transactions
)
SELECT
    ft.is_fraud,
    COUNT(*)                                              AS high_value_transaction_count,
    ROUND(100.0 * COUNT(*) FILTER (WHERE ft.is_fraud = 1) OVER () / NULLIF(COUNT(*) OVER (), 0), 4)
        AS fraud_share_of_high_value_pct,
    AVG(ft.transaction_amt)                               AS avg_high_value_amount
FROM fact_transactions ft, threshold
WHERE ft.transaction_amt >= threshold.p95_amount
GROUP BY ft.is_fraud;
