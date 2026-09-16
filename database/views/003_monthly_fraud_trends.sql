-- View 3: Monthly fraud trends
-- day_index is an ORDINAL day count (not a calendar date — see schema notes),
-- so "month" here is a synthetic 30-day bucket, not a real calendar month.
-- This is stated explicitly rather than silently mislabeled.
CREATE OR REPLACE VIEW v_monthly_fraud_trends AS
SELECT
    (day_index / 30)                                    AS synthetic_month_bucket,
    COUNT(*)                                             AS total_transactions,
    COUNT(*) FILTER (WHERE is_fraud = 1)                 AS fraud_transactions,
    ROUND(100.0 * COUNT(*) FILTER (WHERE is_fraud = 1) / NULLIF(COUNT(*), 0), 4) AS fraud_rate_pct,
    SUM(transaction_amt) FILTER (WHERE is_fraud = 1)     AS fraud_amount
FROM fact_transactions
GROUP BY (day_index / 30)
ORDER BY synthetic_month_bucket;
