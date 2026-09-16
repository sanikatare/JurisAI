-- View 13: Data-quality summary (reads the log table populated after each ETL run)
CREATE OR REPLACE VIEW v_data_quality_summary AS
SELECT
    run_id,
    run_timestamp,
    row_count,
    column_count,
    duplicate_row_count,
    fraud_count,
    fraud_rate_pct,
    row_count - LAG(row_count) OVER (ORDER BY run_timestamp)     AS row_count_delta_vs_prior_run,
    notes
FROM data_quality_log
ORDER BY run_timestamp DESC;
