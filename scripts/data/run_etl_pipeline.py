"""FinSight AI — Reproducible Data ETL & Feature Engineering Runner.

Executes:
Data Validation -> Preprocessing -> Tabular Features -> Temporal Features -> Graph Features.
"""
import sys
import os
import pandas as pd

from src.data.validate import validate
from src.data.clean import clean_data
from src.features.entity_features import extract_entity_features
from src.features.temporal_features import extract_temporal_features
from src.graph.graph_features import compute_leakage_safe_graph_features
from src.utils.logger import get_logger

logger = get_logger("script_etl")


def main():
    print("=" * 60)
    print("      FinSight AI — Data ETL & Feature Pipeline        ")
    print("=" * 60)

    # 1. Load or Generate Input Fixture Data
    raw_path = os.path.join("data", "raw", "sample_transactions.csv")
    if os.path.exists(raw_path):
        logger.info("Loading raw dataset from %s...", raw_path)
        df_raw = pd.read_csv(raw_path)
    else:
        logger.info("Raw dataset not found at %s; generating synthetic IEEE-CIS sample...", raw_path)
        from src.utils.experiment_runner import generate_synthetic_ieee_cis
        df_raw = generate_synthetic_ieee_cis(n_samples=500, random_state=42)
        os.makedirs(os.path.dirname(raw_path), exist_ok=True)
        df_raw.to_csv(raw_path, index=False)

    print(f"[ETL] Input raw DataFrame shape: {df_raw.shape}")

    # 2. Schema Validation
    cfg = {
        "dataset": {
            "id_column": "TransactionID",
            "time_column": "TransactionDT",
            "amount_column": "TransactionAmt",
        }
    }
    val_report = validate(df_raw, cfg)
    print(f"[ETL] Validation Report: {val_report.n_rows} rows, {val_report.duplicate_rows} duplicates.")

    # 3. Data Cleaning
    df_clean = clean_data(df_raw)
    print(f"[ETL] Cleaned DataFrame shape: {df_clean.shape}")

    # 4. Feature Extraction
    df_temp = extract_temporal_features(df_clean)
    df_entity = extract_entity_features(df_temp)
    df_graph = compute_leakage_safe_graph_features(df_entity)

    proc_path = os.path.join("data", "processed", "processed_transactions.csv")
    os.makedirs(os.path.dirname(proc_path), exist_ok=True)
    df_graph.to_csv(proc_path, index=False)
    print(f"[ETL] Processed feature DataFrame saved to {proc_path} (Shape: {df_graph.shape})")
    print("[SUCCESS] ETL and Feature Engineering pipeline executed successfully!")


if __name__ == "__main__":
    main()
