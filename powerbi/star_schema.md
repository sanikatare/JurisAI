# Power BI Star Schema — FinSight AI Phase 2

## Fact grain — the single most important question

**One row in `Fact_Transactions` represents exactly one IEEE-CIS
transaction** (one `TransactionID`), at the moment it was processed —
never an aggregate, never a customer-level or daily-level row. All KPIs
and trend visuals are aggregations OVER this grain, computed by DAX/SQL,
never pre-aggregated into the fact table itself.

## Tables

**Fact_Transactions** (from `fact_transactions` SQL table)
- Grain: 1 row = 1 transaction
- Key measures columns: `transaction_amt`, `is_fraud`, `ml_score` (Phase 3+, currently NULL), `final_risk_score` (Phase 3+, currently NULL)
- Foreign keys: `day_index` → `Dim_Date`, `product_cd` → `Dim_Product_Type`

**Dim_Date**
- Grain: 1 row = 1 `day_index` (an ORDINAL day count derived from `TransactionDT`, not a real calendar date — labeled as such in the model so report viewers aren't misled into thinking these are real dates)
- Primary key: `day_index`
- Attributes: `day_of_week` (cyclical, 0–6)

**Dim_Product_Type**
- Grain: 1 row = 1 `product_cd`
- Primary key: `product_cd`

## Relationships

- `Fact_Transactions[day_index]` → `Dim_Date[day_index]` — many-to-one, single direction
- `Fact_Transactions[product_cd]` → `Dim_Product_Type[product_cd]` — many-to-one, single direction

## Tables intentionally NOT built (see docs/graph_readiness_audit.md)

`Dim_Customer`, `Dim_Merchant`, `Dim_Device`, `Dim_Geography` are **not**
created as Power BI dimension tables in Phase 2. IEEE-CIS has no clean
customer/merchant identity and no confirmed geography granularity —
building these dimensions now would mean modeling fabricated entities.
`card1`, `DeviceType`, and `P_emaildomain` remain as plain attribute
columns on `Fact_Transactions` for slicing, without being promoted to
full dimension tables, until/unless Phase 3+ confirms they behave as
clean, stable entity keys.

## Second fact table for drift monitoring

**Fact_ModelPerformance** (from `fact_model_performance` SQL table) — a
separate, lower-grain fact table (1 row per model evaluation run, not per
transaction) that lets the "model performance over time" dashboard page
(Phase 1 Part 11) exist as first-class BI content rather than a notebook
plot. Empty until Phase 3 produces real evaluation runs — no placeholder
rows are ever inserted.
