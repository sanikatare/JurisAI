# FinSight AI — Data Directory & Pipeline Guidelines

## Overview
This directory structures raw, interim, processed, and sample dataset files used by FinSight AI's ETL pipeline.

---

## Directory Structure
```
data/
├── raw/         # Raw IEEE-CIS Kaggle CSV files (gitignored, see download instructions)
├── interim/     # Cleaned intermediate DataFrames
├── processed/   # Engineered feature DataFrames ready for ML model ingestion
├── features/    # Feature importance matrix & extracted feature maps
├── sample/      # Small synthetic demonstration fixtures for zero-key offline testing
└── README.md
```

## IEEE-CIS Dataset Instructions
1. Download `train_transaction.csv` and `train_identity.csv` from Kaggle: `https://www.kaggle.com/competitions/ieee-fraud-detection/data`
2. Place raw CSV files in `data/raw/`.
3. Run `python scripts/data/run_etl_pipeline.py` to execute schema validation, data cleaning, and feature extraction.
