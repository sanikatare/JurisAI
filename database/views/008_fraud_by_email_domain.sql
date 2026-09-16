-- View 8: Fraud by available "geography-adjacent" entity.
-- IEEE-CIS has no confirmed clean geography field (addr1/addr2 are
-- anonymized region codes of unclear granularity — see graph readiness
-- audit). P_emaildomain is used here instead as the best AVAILABLE proxy
-- with real, documented business meaning (purchaser email provider).
CREATE OR REPLACE VIEW v_fraud_by_email_domain AS
SELECT
    p_email_domain,
    COUNT(*)                                             AS total_transactions,
    COUNT(*) FILTER (WHERE is_fraud = 1)                 AS fraud_transactions,
    ROUND(100.0 * COUNT(*) FILTER (WHERE is_fraud = 1) / NULLIF(COUNT(*), 0), 4) AS fraud_rate_pct
FROM fact_transactions
WHERE p_email_domain IS NOT NULL
GROUP BY p_email_domain
HAVING COUNT(*) >= 30   -- suppress statistically unstable rates on tiny domains
ORDER BY fraud_rate_pct DESC;
