-- View 9: Fraud by available entity (card network / card type — card4/card6)
CREATE OR REPLACE VIEW v_fraud_by_card_type AS
SELECT
    card4                                                 AS card_network,
    card6                                                 AS card_type,
    COUNT(*)                                              AS total_transactions,
    COUNT(*) FILTER (WHERE is_fraud = 1)                  AS fraud_transactions,
    ROUND(100.0 * COUNT(*) FILTER (WHERE is_fraud = 1) / NULLIF(COUNT(*), 0), 4) AS fraud_rate_pct
FROM fact_transactions
GROUP BY card4, card6
ORDER BY fraud_rate_pct DESC NULLS LAST;
