-- View 2: Daily fraud summary
CREATE OR REPLACE VIEW v_daily_fraud_summary AS
SELECT
    day_index,
    COUNT(*) FILTER (WHERE is_fraud = 1)               AS fraud_transactions,
    COUNT(*)                                            AS total_transactions,
    ROUND(100.0 * COUNT(*) FILTER (WHERE is_fraud = 1) / NULLIF(COUNT(*), 0), 4) AS fraud_rate_pct,
    SUM(transaction_amt) FILTER (WHERE is_fraud = 1)    AS fraud_amount
FROM fact_transactions
GROUP BY day_index
ORDER BY day_index;
