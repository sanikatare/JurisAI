-- View 12: Missing-data monitoring
-- Only covers columns that can be NULL post-cleaning (most high-missing
-- columns are dropped in clean.py; this view tracks what remains, per
-- Phase 2 Part 16).
CREATE OR REPLACE VIEW v_missing_data_monitoring AS
SELECT
    COUNT(*)                                              AS total_rows,
    COUNT(*) FILTER (WHERE card1 IS NULL)                 AS card1_missing,
    COUNT(*) FILTER (WHERE card2 IS NULL)                 AS card2_missing,
    COUNT(*) FILTER (WHERE addr1 IS NULL)                 AS addr1_missing,
    COUNT(*) FILTER (WHERE p_email_domain IS NULL)        AS p_email_domain_missing,
    COUNT(*) FILTER (WHERE device_type IS NULL)           AS device_type_missing,
    COUNT(*) FILTER (WHERE ml_score IS NULL)              AS ml_score_missing_awaiting_phase3
FROM fact_transactions;
