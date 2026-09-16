# DAX Measures — FinSight AI Phase 2

12 measures, each with the SQL-equivalent verified against the actual
schema in `sql/schema/001_create_tables.sql`. None of these depend on
Phase 3 model outputs (those are documented separately, ready to add once
`ml_score`/`final_risk_score` are populated).

```dax
Total Transactions = COUNTROWS(Fact_Transactions)

Fraud Transactions = CALCULATE([Total Transactions], Fact_Transactions[is_fraud] = 1)

Non-Fraud Transactions = CALCULATE([Total Transactions], Fact_Transactions[is_fraud] = 0)

Fraud Rate % = DIVIDE([Fraud Transactions], [Total Transactions])

Total Transaction Amount = SUM(Fact_Transactions[transaction_amt])

Fraud Transaction Amount = CALCULATE([Total Transaction Amount], Fact_Transactions[is_fraud] = 1)

Average Transaction Amount = AVERAGE(Fact_Transactions[transaction_amt])

Average Fraud Amount = CALCULATE([Average Transaction Amount], Fact_Transactions[is_fraud] = 1)

Fraud Amount % = DIVIDE([Fraud Transaction Amount], [Total Transaction Amount])

Transactions per Day = DIVIDE([Total Transactions], DISTINCTCOUNT(Fact_Transactions[day_index]))

Fraud Transactions per Day = DIVIDE([Fraud Transactions], DISTINCTCOUNT(Fact_Transactions[day_index]))

Maximum Transaction Amount = MAX(Fact_Transactions[transaction_amt])
```

## Why each measure exists

| Measure | Business question it answers |
|---|---|
| Total Transactions | How much volume are we processing? |
| Fraud Transactions | How many confirmed fraud cases are in the data? |
| Non-Fraud Transactions | Baseline for imbalance context |
| Fraud Rate % | The primary executive KPI — never shown as "accuracy" |
| Total Transaction Amount | Overall financial volume |
| Fraud Transaction Amount | Dollar exposure to fraud |
| Average Transaction Amount | Typical transaction size, context for outlier detection |
| Average Fraud Amount | Do fraud transactions skew larger/smaller than typical? |
| Fraud Amount % | Share of dollar volume attributable to fraud (distinct from Fraud Rate %, which is a COUNT share — the two can diverge meaningfully) |
| Transactions per Day | Volume trend denominator |
| Fraud Transactions per Day | Fraud trend line source |
| Maximum Transaction Amount | Outlier/high-value monitoring |

## Deferred to Phase 3 (documented now so the model is ready, not populated yet)

```dax
-- Only valid once fact_transactions.ml_score / final_risk_score are populated:
Model Precision (Latest) = CALCULATE(MAX(Fact_ModelPerformance[precision_score]), ...)
Model Recall (Latest) = CALCULATE(MAX(Fact_ModelPerformance[recall_score]), ...)
Estimated Loss Prevented = SUMX(FILTER(Fact_Transactions, [final_risk_score] > threshold && is_fraud = 1), [transaction_amt])
```
