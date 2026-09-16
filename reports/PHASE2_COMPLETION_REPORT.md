# FinSight AI — Phase 2 Completion Report

## 1. Dataset used
Primary: **IEEE-CIS Fraud Detection** (`train_transaction.csv` + `train_identity.csv`), per the Phase 1 decision. Not switched — see Part 4 below for why it remains the right choice. Secondary/validation: **PaySim**, wired into `extract.py` as optional, not yet required at this phase.

## 2. Dataset statistics
**Not yet available.** No raw CSVs have been provided to this environment or downloaded (see "Blocking issue" below). `src/data/profile.py` is built, tested-by-construction (schema-agnostic, computes only what it measures), and ready to run the instant the files exist in `data/raw/` — it will produce `reports/data_profile.json` and `reports/data_quality_report.md` with real row/column counts, fraud rate, and imbalance ratio. Nothing here is estimated or invented in place of that.

## 3. Data-quality findings
Not yet measurable for the same reason. The **audit logic** is complete and tested: `src/data/validate.py` checks duplicate rows/IDs, negative/zero amounts, fully-empty columns, constant columns, and invalid (negative) `TransactionDT` values — all against measured data, never assumed. See `tests/test_validate.py` for proof the logic behaves correctly on synthetic data with known-planted issues.

## 4. Leakage findings
Documented qualitatively in `docs/leakage_audit.md` based on IEEE-CIS's publicly known column semantics — flagging C1–C14 and D1–D15 as medium-risk pending Vesta's undisclosed construction details, and codifying the "no future data in rolling features" rule as an enforced, unit-tested constraint (`tests/test_features_leakage.py`) rather than a comment. Empirical leakage checks (e.g. suspiciously high feature importance) are a Phase 3 activity once a model exists.

## 5. Cleaning decisions
Implemented in `src/data/clean.py`: protected columns (target/id/time/amount) are never dropped; fully-empty/constant columns are dropped based on measured properties; columns above a configurable missing-threshold are dropped (excluding protected columns); numeric missingness is imputed with the median **plus an explicit `_was_missing` indicator** (never a blind zero-fill); categorical missingness becomes an explicit `"missing"` category; duplicate rows are flagged and retained, not silently deleted. All decisions are logged to `reports/cleaning_transformation_log.json` on every run. Verified by `tests/test_clean.py` (5/5 passing).

## 6. ETL architecture
`Extract → Validate → Clean → Transform → Load`, implemented as separate, independently testable modules (`src/data/extract.py`, `validate.py`, `clean.py`, `src/features/*`, `load.py`), orchestrated by `src/data/pipeline.py`. Config-driven (`configs/config.yaml`), no hardcoded paths, structured logging to console + file, safe to re-run (extract/validate/clean/transform are pure functions over the raw files; load uses an explicit `if_exists` policy).

## 7. PostgreSQL architecture
`sql/schema/001_create_tables.sql` — see file for full DDL and inline design-rationale comments. Summary: `fact_transactions` (grain: one transaction), `dim_date` (ordinal day index, explicitly NOT a calendar date), `dim_product_type` (from the documented low-cardinality `ProductCD`), `fact_model_performance` and `data_quality_log` for monitoring. No `dim_customer`/`dim_merchant`/`dim_device`/`dim_geography` tables were created — the dataset does not support them without fabrication (see Part 6 of the brief and `docs/graph_readiness_audit.md`).

## 8. Star schema
Documented in `powerbi/star_schema.md`. Fact grain stated explicitly: **one row = one transaction**. Relationships: `Fact_Transactions → Dim_Date` and `Fact_Transactions → Dim_Product_Type`, both many-to-one, single-direction.

## 9. SQL analytics created
All 13 required views implemented in `sql/views/001…013*.sql`: daily transaction summary, daily fraud summary, monthly fraud trends (explicitly labeled as a synthetic 30-day bucket, not a real month), overall fraud rate + imbalance ratio, fraud amount summary, transaction amount statistics (percentiles), fraud by product type, fraud by email domain, fraud by card type, hourly fraud patterns, high-value transaction analysis (threshold = measured p95, not a hardcoded dollar figure), missing-data monitoring, and data-quality-log summary.

## 10. Key business insights
**Not yet available** — every insight in Phase 1 Part 9 (fraud rate, amount patterns, temporal patterns, category-level fraud rates) requires running the views above against loaded data. This report does not fabricate placeholder findings. Once data is loaded, run the queries in `sql/views/` and populate this section with real numbers, phrased as "associated with" / "observed pattern," never "causes," per the Phase 1 instruction.

## 11. Feature engineering created
`src/features/temporal_features.py`: `tx_hour_of_day`, `tx_day_of_cycle`, `tx_day_index` (pure functions of each row's own timestamp — zero leakage risk, verified by test); `time_since_prev_tx` (leakage-safe via per-entity `.diff()`); `chronological_split_indices` (strict time-ordered train/val/test split, no shuffling, verified by test). `src/features/entity_features.py`: `add_entity_rolling_features` (prior-transaction-count and prior-amount statistics via `.shift(1)` + `.expanding()`, verified by test to exclude the current row); `add_shared_identifier_flags` (explicitly labeled EDA-only, unsafe for Phase 3 modeling without recomputation — see leakage audit).

## 12. Temporal analysis
Methodology built (`chronological_split_indices`), but the actual fraud-distribution-over-time report requires real `TransactionDT` values. `docs/leakage_audit.md` and `configs/config.yaml` (`temporal:` section) establish the 60/20/20 chronological split Phase 1 RQ3 requires. Run against real data before Phase 3 begins.

## 13. Graph readiness assessment
Full table and **Conditional GO** recommendation in `docs/graph_readiness_audit.md`. Summary: `card1` is the strongest available entity-graph key; a full multi-entity-type graph (Customer/Merchant/Location nodes) is **not supported** by this dataset without fabricating identities, so the realistic Phase 3/4 design is a single-entity-type transaction graph linked via shared `card1`/normalized `DeviceInfo`/`P_emaildomain`. Full GNN is explicitly deferred pending Experiment 4 (graph-feature) results, consistent with Phase 1 Part 14's own instruction not to default to GNN for its own sake.

## 14. Power BI architecture
`powerbi/star_schema.md` — fact grain, tables, relationships, and the explicit list of dimension tables NOT built and why.

## 15. DAX measures
12 measures implemented and explained in `powerbi/dax_measures.md`, plus 3 Phase-3-deferred measures documented (not implemented, since they depend on unpopulated `ml_score`/`final_risk_score` columns).

## 16. Tests performed
12 pytest tests across 3 files, **all passing** (verified by actually running `pytest` in this environment, not just written):
- `tests/test_clean.py` (5 tests) — column dropping, protected-column preservation (caught and fixed a real bug during this phase — see Part 17 below), missingness-indicator imputation, duplicate flagging.
- `tests/test_features_leakage.py` (4 tests) — the leakage-specific suite: relative-time correctness, time-since-previous-transaction correctness, entity rolling-mean excludes the current row, chronological split never shuffles.
- `tests/test_validate.py` (3 tests) — duplicate-ID detection, negative-amount flagging without row deletion, empty/constant column detection.

## 17. Problems encountered
1. **No dataset available in this environment.** IEEE-CIS is a Kaggle competition dataset requiring authenticated download; this tool has no Kaggle access and none was uploaded. Per the brief's explicit instruction, this is disclosed rather than worked around with synthetic substitute data pretending to be real. See "Blocking issue" below for exact next steps.
2. **A real bug was found and fixed during testing:** the initial `clean()` implementation dropped a column as "constant" if a high-missingness protected column happened to reduce to a single observed value — which would have silently deleted `TransactionAmt` under certain missingness patterns. Caught by `test_never_drops_protected_columns_even_if_high_missing`, fixed by moving the `protected` set definition before, and into, the constant/empty-column drop step. This is exactly the kind of bug the Phase 2 testing requirement (Part 20) exists to catch before it reaches Phase 3.

## 18. Decisions made
- Kept IEEE-CIS as primary dataset (Phase 1 decision affirmed, not overridden — see Part 4 below).
- Stored the 339 V-columns + C/D/M-columns as a single JSONB column rather than ~377 flat columns, to keep the business-facing schema usable while preserving full fidelity for Phase 3 ML.
- Did not build `dim_customer`/`dim_merchant`/`dim_device`/`dim_geography` — no dataset support without fabrication.
- Treated `card1` as the leading graph-entity candidate, deferred a final GNN decision to Phase 3 pending Experiment 4 evidence.
- Chose median+indicator imputation and explicit-category imputation over blind fills, per the brief's explicit prohibition on blind zero-fills.

## 19. Files created
Full repository under `FinSight-AI/` (see the file tree in `README.md`): `README.md`, `requirements.txt`, `.env.example`, `.gitignore`, `pytest.ini`, `configs/config.yaml`, `src/{data,features,database,utils}/*.py` (11 modules), `sql/schema/001_create_tables.sql`, `sql/views/001–013*.sql` (13 views), `tests/*.py` (3 files, 12 tests), `docs/{data_dictionary,leakage_audit,graph_readiness_audit}.md`, `powerbi/{star_schema,dax_measures}.md`, this report.

## 20. Phase 2 acceptance checklist

- [x] Dataset structure is verified — **against public documentation**, not yet against actual files (blocked on data availability, not on missing work)
- [ ] Data quality is measured — blocked on data availability; measurement code is built and tested
- [x] Leakage risks are documented (`docs/leakage_audit.md`)
- [x] ETL can be rerun (config-driven, pure functions, explicit `if_exists` load policy)
- [ ] PostgreSQL database works — schema is written and reviewed; not yet applied against a live instance in this environment (no Postgres server provisioned here)
- [ ] Clean data is loaded — blocked on data availability
- [ ] SQL views work — written and reviewed against the schema; not yet executed against live data (blocked on data + DB availability)
- [ ] Analytical queries produce meaningful results — blocked on data availability
- [x] Temporal ordering is preserved (chronological split implemented and unit-tested)
- [x] Feature engineering avoids future leakage (implemented AND verified by dedicated leakage tests)
- [x] Graph readiness is assessed (`docs/graph_readiness_audit.md`, conditional GO)
- [x] Power BI model is logically correct (star schema + grain explicitly defined)
- [x] DAX measures are validated — validated against the real schema's column names/types; not yet validated against real numbers (blocked on data availability)
- [x] Basic tests pass (12/12, verified by execution in this environment)
- [ ] Phase 3 ML can start without redesigning the data layer — **not yet confirmed**, since the data layer has never been run against real data end-to-end

## 21. Phase 3 readiness assessment

# **NOT READY**

**Technical reasons:**
1. The entire data engineering foundation (ETL, schema, views, feature logic) is built, code-reviewed via its own test suite, and passing — but it has **never been executed against the real IEEE-CIS dataset**, because that dataset is not present in this environment and was not provided. "Tests pass on synthetic fixtures" is necessary but not sufficient evidence that the real pipeline works end-to-end (e.g. real column names, real missingness patterns, real cardinalities could surface issues the synthetic fixtures don't cover).
2. No PostgreSQL instance has been provisioned/connected in this environment, so `sql/schema/001_create_tables.sql` and the 13 views have been reviewed but not executed against a live database.
3. Every numeric claim required by Phase 2 Parts 2, 3, 9, 11, and 12's final confirmation depends on real data that doesn't exist here yet.

**What you need to do before Phase 3 starts (in order):**
1. Download IEEE-CIS from `https://www.kaggle.com/competitions/ieee-fraud-detection/data` and place the 4 files in `data/raw/` (exact names in `README.md`).
2. Run `python -m src.data.profile` and review `reports/data_quality_report.md` — fill in the TBD cells in `docs/data_dictionary.md` and `docs/graph_readiness_audit.md` with real numbers.
3. Provision a PostgreSQL instance, fill in `.env` from `.env.example`, run `psql -f sql/schema/001_create_tables.sql` then each file in `sql/views/`.
4. Run `python -m src.data.pipeline --config configs/config.yaml --load` and confirm row counts in Postgres match the profiled raw counts.
5. Run each SQL view manually and sanity-check at least the fraud rate, total transaction count, and imbalance ratio against `reports/data_quality_report.md` — they must match.
6. Re-run `pytest tests/ -v` (should still be 12/12 — the synthetic tests are independent of the real data) and confirm no regressions were introduced while wiring in real data.
7. Only once steps 1–6 all produce real, verified numbers should Phase 3 (ML) begin — at that point, tell me to start Phase 3 and I will pick up from a genuinely verified data foundation instead of an untested one.

**Once you've done that, come back and I can:** run the actual profiling/EDA against your real data, finalize the data dictionary and graph-readiness numbers, and then proceed to Phase 3 (baseline ML models, Experiments 1–2 from the Phase 1 blueprint).
