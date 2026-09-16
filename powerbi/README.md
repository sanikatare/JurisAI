# Power BI Analytics Architecture — FinSight AI

## 1. Overview
Power BI serves as the primary downstream business analytics layer for FinSight AI, consuming model predictions, risk tiers, and performance drift metrics from PostgreSQL.

---

## 2. Data Sources & Table Grain
- **`Fact_Transactions`** (from `fact_transactions`): Grain = 1 row per transaction.
- **`Fact_ModelPredictions`** (from `fact_model_predictions`): Grain = 1 row per model prediction run.
- **`Fact_ModelPerformance`** (from `fact_model_performance`): Grain = 1 row per evaluation run.
- **`Dim_Date`**: Ordinal day index.
- **`Dim_Product_Type`**: Product category code (`ProductCD`).

---

## 3. Relationships & Measures
- `Fact_Transactions[day_index]` $\to$ `Dim_Date[day_index]` (Many-to-One, Single direction).
- `Fact_Transactions[product_cd]` $\to$ `Dim_Product_Type[product_cd]` (Many-to-One, Single direction).
- Key DAX Measures documented in [powerbi/dax_measures.md](file:///c:/Users/DELL/Downloads/JURIS/FinSight-AI/powerbi/dax_measures.md).
