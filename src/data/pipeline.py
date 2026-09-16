"""Reproducible ETL orchestrator — Phase 2 Part 5.

Extract -> Validate -> Clean -> Transform -> (optionally) Load

Usage:
    python -m src.data.pipeline --config configs/config.yaml
    python -m src.data.pipeline --config configs/config.yaml --load   # also writes to Postgres

Safe to re-run: extract/validate/clean/transform are pure functions over
the raw files (no in-place mutation of data/raw/), and load() uses an
explicit if_exists policy rather than silently duplicating rows on rerun.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from src.data.clean import clean
from src.data.extract import extract_train, RawDataNotFoundError
from src.data.validate import validate
from src.features.temporal_features import add_relative_time_features
from src.utils.config import load_config
from src.utils.logger import get_logger

logger = get_logger("pipeline")


def run(config: dict, do_load: bool = False) -> pd.DataFrame:
    target_col = config["dataset"]["target_column"]
    time_col = config["dataset"]["time_column"]

    logger.info("STEP 1/5: extract")
    try:
        raw_df = extract_train(config)
    except RawDataNotFoundError as e:
        logger.error(str(e))
        raise

    logger.info("STEP 2/5: validate")
    validation_report = validate(raw_df, config)
    reports_dir = Path(config["paths"]["reports_dir"])
    reports_dir.mkdir(parents=True, exist_ok=True)
    (reports_dir / "validation_report.json").write_text(
        json.dumps(validation_report.as_dict(), indent=2, default=str), encoding="utf-8"
    )

    logger.info("STEP 3/5: clean")
    cleaned_df, transform_log = clean(raw_df, config, target_col)
    (reports_dir / "cleaning_transformation_log.json").write_text(
        json.dumps(transform_log.steps, indent=2, default=str), encoding="utf-8"
    )

    interim_dir = Path(config["paths"]["interim_dir"])
    interim_dir.mkdir(parents=True, exist_ok=True)
    cleaned_df.to_parquet(interim_dir / "cleaned_transactions.parquet", index=False)
    logger.info("Wrote interim cleaned dataset: %s rows, %s cols",
                *cleaned_df.shape)

    logger.info("STEP 4/5: transform (feature engineering foundation)")
    feature_df = add_relative_time_features(cleaned_df, time_col)
    # Entity-level rolling features are NOT applied blindly here — they
    # require a confirmed entity key from the graph readiness audit
    # (docs/graph_readiness_audit.md). Once that key is confirmed against
    # the real data, call src.features.entity_features.add_entity_rolling_features
    # explicitly with that column name.

    processed_dir = Path(config["paths"]["processed_dir"])
    processed_dir.mkdir(parents=True, exist_ok=True)
    feature_df.to_parquet(processed_dir / "feature_ready_transactions.parquet", index=False)
    logger.info("Wrote processed feature-ready dataset: %s rows, %s cols",
                *feature_df.shape)

    if do_load:
        logger.info("STEP 5/5: load")
        from src.data.load import load_fact_transactions
        from src.database.engine import get_engine
        engine = get_engine()
        load_fact_transactions(feature_df, engine)
    else:
        logger.info("STEP 5/5: load skipped (pass --load to write to Postgres)")

    return feature_df


def main() -> None:
    parser = argparse.ArgumentParser(description="FinSight AI Phase 2 ETL pipeline")
    parser.add_argument("--config", default="configs/config.yaml")
    parser.add_argument("--load", action="store_true", help="Also load into Postgres")
    args = parser.parse_args()

    config = load_config(args.config)
    run(config, do_load=args.load)


if __name__ == "__main__":
    main()
