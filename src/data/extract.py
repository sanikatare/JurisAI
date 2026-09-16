"""Extract stage of the ETL pipeline.

Reads the raw IEEE-CIS CSVs from data/raw/ and merges transaction + identity
tables on TransactionID (a left join, since IEEE-CIS identity coverage is
partial by design — most transactions have no matching identity row).

This module makes NO assumptions about columns beyond the join key and the
columns named explicitly in configs/config.yaml (target/id/time/amount).
Every other column is passed through as-is; nothing is invented or dropped
here — dropping happens later, in clean.py, based on MEASURED properties.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.utils.logger import get_logger

logger = get_logger("extract")


class RawDataNotFoundError(FileNotFoundError):
    """Raised when required raw files are missing, with download instructions."""


DOWNLOAD_INSTRUCTIONS = """
Required raw files are missing from data/raw/.

Download the IEEE-CIS Fraud Detection dataset from:
    https://www.kaggle.com/competitions/ieee-fraud-detection/data
(requires a free Kaggle account + accepting the competition rules)

Place these files in data/raw/:
    train_transaction.csv
    train_identity.csv
    test_transaction.csv   (optional for Phase 2 profiling, has no isFraud label)
    test_identity.csv      (optional for Phase 2 profiling)

Missing file(s): {missing}
"""


def _require_files(raw_dir: Path, filenames: list[str]) -> None:
    missing = [f for f in filenames if not (raw_dir / f).exists()]
    if missing:
        raise RawDataNotFoundError(DOWNLOAD_INSTRUCTIONS.format(missing=missing))


def extract_train(config: dict) -> pd.DataFrame:
    """Load and merge train_transaction.csv + train_identity.csv.

    Only the training files are used for Phase 2 profiling/EDA/leakage work,
    since only they contain the isFraud label needed for target analysis.
    """
    raw_dir = Path(config["paths"]["raw_dir"])
    tx_file = config["files"]["train_transaction"]
    id_file = config["files"]["train_identity"]
    _require_files(raw_dir, [tx_file, id_file])

    id_col = config["dataset"]["id_column"]

    logger.info("Reading %s", tx_file)
    transactions = pd.read_csv(raw_dir / tx_file)
    logger.info("transactions shape: %s", transactions.shape)

    logger.info("Reading %s", id_file)
    identity = pd.read_csv(raw_dir / id_file)
    logger.info("identity shape: %s", identity.shape)

    merged = transactions.merge(identity, on=id_col, how="left", validate="one_to_one")
    logger.info("merged shape: %s (left join preserves all %s transaction rows)",
                merged.shape, len(transactions))

    return merged


def extract_paysim(config: dict) -> pd.DataFrame | None:
    """Load the PaySim secondary/validation dataset, if present.

    Returns None (does not raise) if PaySim hasn't been downloaded yet —
    PaySim is optional for Phase 2 and only required once Phase 3 wants to
    validate graph-feature findings on a second dataset (Phase 1, Part 10).
    """
    raw_dir = Path(config["paths"]["raw_dir"])
    paysim_file = config["files"]["paysim"]
    path = raw_dir / paysim_file
    if not path.exists():
        logger.warning("PaySim file not found at %s — skipping (optional at Phase 2).", path)
        return None
    df = pd.read_csv(path)
    logger.info("PaySim shape: %s", df.shape)
    return df
