# FinSight AI — Data Dictionary (IEEE-CIS Fraud Detection)

**Status of this document:** built from the IEEE-CIS competition's public,
documented column descriptions (stable, well-known information about this
dataset). Columns marked **TBD** in Missing % / Unique Count are exactly
that — genuinely unknown until `python -m src.data.profile` is run against
the real `train_transaction.csv` + `train_identity.csv` files. Nothing in
this document invents a number; unmeasured cells say so explicitly.

| Field | Business Meaning | Technical Meaning | Data Type | Source Table | Observed Values | Missing % | Transformation | ML Use | Analytics Use | Graph Use | Potential Leakage | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TransactionID | Unique transaction reference | Primary key | Integer | transaction | Sequential unique IDs | TBD (expected ~0%) | None (protected) | Join key | Join key | Node ID (Transaction) | None | Never used as a model feature itself |
| isFraud | Whether the transaction was fraudulent | Binary target label | Integer (0/1) | transaction | 0, 1 | TBD (expected 0% in train, absent in test) | None (protected) | Target | Fraud rate KPI | Node label | **This IS the target — never a feature** | Only present in train_transaction.csv |
| TransactionDT | Time elapsed reference | Relative seconds-elapsed timestamp from an arbitrary reference point (NOT a calendar date) | Integer (seconds) | transaction | Monotonic non-negative | TBD (expected 0%) | Derive tx_hour_of_day, tx_day_of_cycle, day_index | Temporal split key | Time-series trend axis | Edge ordering | Must never derive a feature using a LATER TransactionDT than the row being scored | No public mapping to real calendar dates exists |
| TransactionAmt | Purchase amount | Transaction value | Numeric (float) | transaction | Non-negative, TBD range | TBD (expected 0%) | None / behavioral aggregates | Core numeric feature | Total/avg fraud value KPIs | Risk-engine amount factor | Low (amount is legitimately known at prediction time) | Verify no negative/zero values once real data loaded (validate.py checks this) |
| ProductCD | Product category code | Categorical product type | String | transaction | Documented as a small set incl. W, C, R, H, S | TBD (expected 0%) | None | Categorical feature (one-hot/target-encoded) | `dim_product_type`, fraud-by-category view | N/A | None | Confirm actual category set against real data before finalizing `dim_product_type` rows |
| card1–card6 | Card/account identifying attributes | Anonymized card metadata (card1/2/3/5 numeric identifiers/limits, card4 network, card6 type) | Mixed | transaction | TBD | TBD | card1 candidate entity key (graph audit) | Categorical/numeric features | Card-type breakdown view | **card1 is the leading candidate transaction-graph entity key** | High-cardinality — not a clean "customer ID"; anonymized proxy only |
| addr1, addr2 | Billing address region codes | Anonymized address-region codes | Numeric | transaction | TBD | TBD (documented as often missing) | Categorical feature | Limited — granularity unclear | Weak | None | Do NOT treat as a real "state/country" field without confirming granularity |
| dist1, dist2 | Distance metrics | Undisclosed distance calculation (e.g. billing-to-shipping) | Numeric | transaction | TBD | TBD (documented as heavily missing) | Numeric feature if missingness is tractable | Weak | Weak | None | Confirm real missing % — may fall above the drop threshold |
| P_emaildomain | Purchaser email domain | Email provider of the purchaser | String | transaction | e.g. gmail.com, yahoo.com, etc. (documented) | TBD (documented as partially missing) | Categorical feature | Fraud-by-domain view (v_fraud_by_email_domain) | Shared-domain graph signal | Low-moderate | Best available "geography-adjacent" business dimension |
| R_emaildomain | Recipient email domain | Email provider of the recipient | String | transaction | Similar to P_emaildomain | TBD (documented as heavily missing) | Categorical feature | Secondary domain analysis | Shared-domain graph signal | Low-moderate | Often null when purchaser=recipient |
| C1–C14 | Vesta engineered counting features | Undisclosed counts (e.g. related addresses/devices) | Numeric | transaction | TBD | TBD | Numeric ML features (JSONB) | Not individually interpretable | Weak (already aggregated by Vesta) | None known | Anonymized — do not assign a false business meaning |
| D1–D15 | Vesta engineered time-delta features | Undisclosed time deltas (e.g. days since prior transaction) | Numeric | transaction | TBD | TBD (documented as variably missing) | Numeric ML features (JSONB) | Not individually interpretable | Weak | Possible overlap with our own time_since_prev_tx feature — compare, don't duplicate blindly | Anonymized |
| M1–M9 | Vesta engineered match flags | Undisclosed true/false match indicators (e.g. name-on-card matches billing name) | Categorical (T/F/NaN) | transaction | T, F, NaN | TBD | Categorical ML features (JSONB) | Not individually interpretable | Weak | None known | Anonymized |
| V1–V339 | Vesta engineered/ranked features | Undisclosed engineered features, PCA/ranking-style | Numeric | transaction | TBD | TBD (many documented as heavily missing/grouped) | Numeric ML features (JSONB) | Primary ML signal historically (per public competition writeups) | Not usable in business-facing BI (uninterpretable) | None known | Anonymized — stored in `raw_engineered_features` JSONB rather than 339 flat columns |
| id_01–id_38 | Identity/device signals | Undisclosed identity-verification signals | Mixed | identity | TBD | TBD (identity table only covers a minority of transactions — documented) | Numeric/categorical ML features | Weak (anonymized) | Device/identity graph signal | Anonymized |
| DeviceType | Device category | e.g. desktop/mobile | String | identity | desktop, mobile (documented) | TBD (only present for identity-matched rows) | Categorical feature | Device breakdown | Shared-device graph signal | None | Coverage is PARTIAL by dataset design, not a data-quality defect |
| DeviceInfo | Device description string | Free-text device/browser string | String | identity | TBD (high cardinality, messy) | TBD | Needs normalization before use | Weak until cleaned | Shared-device graph signal (candidate) | None | High cardinality; candidate for a `device_fingerprint` key after normalization |

## Fields explicitly excluded from the analytical schema

The 339 V-columns, 14 C-columns, 15 D-columns, and 9 M-columns are stored
as a single `raw_engineered_features` JSONB column on `fact_transactions`
(see `sql/schema/001_create_tables.sql`) rather than as ~377 individual
columns. Reasoning: they are Vesta's anonymized, non-independently-
interpretable engineered features (this is publicly documented about the
dataset), so exposing them as flat business-facing columns would not
serve Power BI/analyst consumers, while still needing full fidelity for
Phase 3 ML — JSONB satisfies both without schema bloat.

## Next step to complete this document

Run `python -m src.data.profile` once the real CSVs are in `data/raw/`,
then copy the real Missing % and Unique Count values from
`reports/data_quality_report.md` into the TBD cells above.
