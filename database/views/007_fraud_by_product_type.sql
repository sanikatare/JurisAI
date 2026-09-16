-- View 7: Fraud by category (ProductCD is the only confirmed, documented
-- low-cardinality categorical dimension available — see schema notes).
CREATE OR REPLACE VIEW v_fraud_by_product_type AS
SELECT
    product_cd,
    COUNT(*)                                             AS total_transactions,
    COUNT(*) FILTER (WHERE is_fraud = 1)                 AS fraud_transactions,
    ROUND(100.0 * COUNT(*) FILTER (WHERE is_fraud = 1) / NULLIF(COUNT(*), 0), 4) AS fraud_rate_pct
FROM fact_transactions
GROUP BY product_cd
ORDER BY fraud_rate_pct DESC NULLS LAST;
