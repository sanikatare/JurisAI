"""Load stage — writes processed data into PostgreSQL.

Applies the schema defined in sql/schema/001_create_tables.sql. This
module assumes that schema has already been applied (see README "Running
the pipeline" step 3) — it does not run DDL itself, to keep schema
migrations explicit and reviewable rather than implicit in Python code.
"""
from __future__ import annotations

import pandas as pd
from sqlalchemy.engine import Engine

from src.utils.logger import get_logger

logger = get_logger("load")


def load_fact_transactions(df: pd.DataFrame, engine: Engine, if_exists: str = "append") -> int:
    """Load the cleaned/feature-ready transaction table into fact_transactions.

    Model-output columns (ml_score, anomaly_score, graph_risk_score,
    final_risk_score, risk_tier) are intentionally NOT populated here —
    Phase 2 produces no model outputs. They exist in the schema (as
    nullable columns) so Phase 3 can UPDATE this table by TransactionID
    once real scores exist, rather than requiring a schema change later.
    """
    n = df.to_sql(
        "fact_transactions",
        engine,
        if_exists=if_exists,
        index=False,
        chunksize=5000,
        method="multi",
    )
    logger.info("Loaded %s rows into fact_transactions (if_exists=%s)", len(df), if_exists)
    return len(df)


def load_dim_date(dates: pd.DataFrame, engine: Engine) -> int:
    dates.to_sql("dim_date", engine, if_exists="append", index=False, method="multi")
    logger.info("Loaded %s rows into dim_date", len(dates))
    return len(dates)
