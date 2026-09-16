-- FinSight AI — Phase 2 PostgreSQL schema
--
-- Design notes (Phase 2, Part 6 & 7):
--
-- 1. We do NOT create dim_customer, dim_merchant, dim_device, or
--    dim_geography tables. IEEE-CIS does not contain a real customer ID,
--    merchant name, device table, or geographic field with confirmed low
--    cardinality/clean structure — card1-card6, DeviceInfo, addr1/addr2 are
--    partial, high-cardinality, and privacy-anonymized proxies, not clean
--    entity tables. Building fake dimension tables around them would
--    violate the explicit Phase 2 instruction. See
--    docs/graph_readiness_audit.md for the entity-by-entity justification.
--
-- 2. dim_product_type IS created because ProductCD is documented as a
--    small, stable set of categories (W, C, R, H, S) — a genuine,
--    low-cardinality dimension.
--
-- 3. dim_date IS created from TransactionDT (relative seconds-elapsed),
--    NOT a real calendar date — see column comments below.
--
-- 4. The ~339 anonymized V-columns, 14 C-columns, 15 D-columns and 9
--    M-columns are Vesta's engineered, PCA-style anonymized features.
--    They carry no independently interpretable business meaning (this is
--    publicly documented about IEEE-CIS), so they do not belong in a
--    business-facing star schema. They are stored as a single JSONB
--    column (raw_engineered_features) on fact_transactions so Phase 3 ML
--    work can access them in full without bloating the analytical table
--    with 339 mostly-sparse columns that Power BI users would never touch.
--
-- 5. ml_score / anomaly_score / graph_risk_score / final_risk_score /
--    risk_tier are included as NULLABLE columns now (per Phase 1 Part 15
--    / Phase 2 Part 6) but are NOT populated by Phase 2. Phase 3+ will
--    UPDATE fact_transactions SET ml_score = ... WHERE transaction_id = ...
--    once real model outputs exist. No fake/placeholder values are ever
--    written to these columns.

CREATE TABLE IF NOT EXISTS dim_product_type (
    product_cd      VARCHAR(4) PRIMARY KEY,     -- e.g. 'W','C','R','H','S' — confirm actual values against real data
    description     TEXT
);

CREATE TABLE IF NOT EXISTS dim_date (
    day_index       INTEGER PRIMARY KEY,        -- TransactionDT // 86400 — an ORDINAL day count, not a calendar date
    day_of_week     SMALLINT NOT NULL,          -- 0-6, cyclical only; cannot be mapped to a real weekday without a reference date Vesta never published
    hour_bucket_note TEXT DEFAULT 'hour-of-day is stored per-transaction on fact_transactions (tx_hour_of_day), not here, since it varies within a day_index'
);

CREATE TABLE IF NOT EXISTS fact_transactions (
    transaction_id              BIGINT PRIMARY KEY,          -- TransactionID (confirmed unique per validate.py)
    is_fraud                    SMALLINT NOT NULL,            -- isFraud: 0/1, target label (train data only)
    transaction_dt              BIGINT NOT NULL,              -- raw relative seconds-elapsed timestamp
    day_index                   INTEGER REFERENCES dim_date(day_index),
    tx_hour_of_day               SMALLINT,                     -- 0-23, derived in src/features/temporal_features.py
    transaction_amt              NUMERIC(12, 2) NOT NULL,      -- TransactionAmt
    product_cd                   VARCHAR(4) REFERENCES dim_product_type(product_cd),
    card1                         INTEGER,                      -- high-cardinality proxy identifier — kept as a plain column, NOT a dimension (see note above)
    card2                         INTEGER,
    card3                         INTEGER,
    card4                         VARCHAR(20),                  -- card network, e.g. visa/mastercard — confirm actual values
    card5                         INTEGER,
    card6                         VARCHAR(20),                  -- card type, e.g. debit/credit — confirm actual values
    addr1                         INTEGER,
    addr2                         INTEGER,
    dist1                         NUMERIC(12, 2),
    dist2                         NUMERIC(12, 2),
    p_email_domain                VARCHAR(50),
    r_email_domain                VARCHAR(50),
    device_type                   VARCHAR(20),                  -- from identity table, partial coverage
    device_info                   VARCHAR(100),
    raw_engineered_features       JSONB,                         -- all V*/C*/D*/M* columns as key-value pairs, full fidelity for Phase 3 ML

    -- Phase 3+ model outputs — NULL until real models exist. See note 5 above.
    ml_score                      NUMERIC(6, 5),
    anomaly_score                 NUMERIC(6, 5),
    graph_risk_score              NUMERIC(6, 5),
    final_risk_score              NUMERIC(6, 5),
    risk_tier                     VARCHAR(10) CHECK (risk_tier IN ('Low','Medium','High','Critical') OR risk_tier IS NULL),
    model_version                 VARCHAR(50),                   -- which model/run produced the scores above, for lineage (RQ4)

    loaded_at                     TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_fact_transactions_day_index ON fact_transactions(day_index);
CREATE INDEX IF NOT EXISTS idx_fact_transactions_is_fraud ON fact_transactions(is_fraud);
CREATE INDEX IF NOT EXISTS idx_fact_transactions_card1 ON fact_transactions(card1);
CREATE INDEX IF NOT EXISTS idx_fact_transactions_product_cd ON fact_transactions(product_cd);

-- Supports Phase 1 Part 16 (concept drift monitoring) — a first-class BI
-- object rather than something buried in a notebook, per Phase 1 Part 11.
CREATE TABLE IF NOT EXISTS fact_model_performance (
    evaluation_id     SERIAL PRIMARY KEY,
    model_version      VARCHAR(50) NOT NULL,
    evaluation_window_start INTEGER,     -- day_index
    evaluation_window_end   INTEGER,     -- day_index
    precision_score     NUMERIC(6,5),
    recall_score         NUMERIC(6,5),
    f1_score              NUMERIC(6,5),
    pr_auc                NUMERIC(6,5),
    evaluated_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Supports Phase 2 Part 16 (data quality monitoring), regenerated after each ETL run.
CREATE TABLE IF NOT EXISTS data_quality_log (
    run_id             SERIAL PRIMARY KEY,
    run_timestamp       TIMESTAMPTZ NOT NULL DEFAULT now(),
    row_count            INTEGER NOT NULL,
    column_count          INTEGER NOT NULL,
    duplicate_row_count    INTEGER NOT NULL,
    fraud_count             INTEGER NOT NULL,
    fraud_rate_pct           NUMERIC(6,4) NOT NULL,
    notes                     TEXT
);
