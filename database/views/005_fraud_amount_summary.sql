-- View 5: Fraud amount summary
CREATE OR REPLACE VIEW v_fraud_amount_summary AS
SELECT
    SUM(transaction_amt) FILTER (WHERE is_fraud = 1)   AS total_fraud_amount,
    AVG(transaction_amt) FILTER (WHERE is_fraud = 1)   AS avg_fraud_amount,
    MAX(transaction_amt) FILTER (WHERE is_fraud = 1)   AS max_fraud_amount,
    SUM(transaction_amt) FILTER (WHERE is_fraud = 0)   AS total_legitimate_amount,
    AVG(transaction_amt) FILTER (WHERE is_fraud = 0)   AS avg_legitimate_amount
FROM fact_transactions;
