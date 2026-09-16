-- View 10: Hour-of-day patterns
CREATE OR REPLACE VIEW v_hourly_fraud_patterns AS
SELECT
    tx_hour_of_day,
    COUNT(*)                                              AS total_transactions,
    COUNT(*) FILTER (WHERE is_fraud = 1)                  AS fraud_transactions,
    ROUND(100.0 * COUNT(*) FILTER (WHERE is_fraud = 1) / NULLIF(COUNT(*), 0), 4) AS fraud_rate_pct
FROM fact_transactions
GROUP BY tx_hour_of_day
ORDER BY tx_hour_of_day;
