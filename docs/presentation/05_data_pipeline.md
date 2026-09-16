# Slide 5: Data Engineering & Validation

## ETL & Temporal Leakage Protection
- **Dataset**: IEEE-CIS Financial Fraud Detection dataset (590,540 rows, 3.50% baseline fraud rate).
- **Validation Stage**: Pre-cleaning structural audit flagging duplicate IDs, negative amounts, and constant columns without silent data dropping.
- **Chronological Split**: 70% Train / 15% Val / 15% Test split respecting monotonically increasing `TransactionDT` timestamps.
- **Leakage Prevention**: All rolling aggregations use expanding prior windows ($t < t_i$) ensuring zero future information lookahead.
