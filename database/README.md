# FinSight AI — Database Architecture & PostgreSQL Schemas

## Overview
This directory contains the PostgreSQL relational star schema definitions (`database/schema/`) and analytical views (`database/views/`) supporting FinSight AI's data engineering, ML predictions, monitoring logs, and Power BI dashboards.

---

## Directory Structure
```
database/
├── schema/
│   ├── 001_create_tables.sql       # Core Relational Tables & Star Schema
│   ├── 002_create_ml_tables.sql    # ML Prediction Fact & SHAP Attribution Tables
│   └── 003_create_monitoring_tables.sql # Fact Monitoring & PSI Drift Tables
├── views/
│   ├── 001_daily_transaction_summary.sql ... 015_model_performance_view.sql # 15 Analytical Views
└── README.md
```

---

## Schema DDL Summary
1. `001_create_tables.sql`: `fact_transactions` (grain: one row per transaction), `dim_cards`, `dim_devices`, `dim_products`.
2. `002_create_ml_tables.sql`: `fact_model_predictions`, `fact_shap_attributions`.
3. `003_create_monitoring_tables.sql`: `fact_model_monitoring`, `fact_data_drift`.
