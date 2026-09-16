-- View 6: Transaction amount statistics (distribution overview)
CREATE OR REPLACE VIEW v_transaction_amount_statistics AS
SELECT
    is_fraud,
    COUNT(*)                                            AS n,
    MIN(transaction_amt)                                 AS min_amount,
    percentile_cont(0.25) WITHIN GROUP (ORDER BY transaction_amt) AS p25_amount,
    percentile_cont(0.50) WITHIN GROUP (ORDER BY transaction_amt) AS median_amount,
    percentile_cont(0.75) WITHIN GROUP (ORDER BY transaction_amt) AS p75_amount,
    percentile_cont(0.95) WITHIN GROUP (ORDER BY transaction_amt) AS p95_amount,
    percentile_cont(0.99) WITHIN GROUP (ORDER BY transaction_amt) AS p99_amount,
    MAX(transaction_amt)                                 AS max_amount,
    AVG(transaction_amt)                                 AS mean_amount,
    STDDEV(transaction_amt)                              AS stddev_amount
FROM fact_transactions
GROUP BY is_fraud;
