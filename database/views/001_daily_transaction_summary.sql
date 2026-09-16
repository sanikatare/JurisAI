-- View 1: Daily transaction summary
-- One row per day_index. Supports "transaction volume trend" (Phase 2 Part 13).
CREATE OR REPLACE VIEW v_daily_transaction_summary AS
SELECT
    day_index,
    COUNT(*)                       AS total_transactions,
    SUM(transaction_amt)           AS total_transaction_value,
    AVG(transaction_amt)           AS avg_transaction_amount,
    MAX(transaction_amt)           AS max_transaction_amount
FROM fact_transactions
GROUP BY day_index
ORDER BY day_index;
