"""Temporal feature engineering — Phase 2 Part 10/11.

TransactionDT in IEEE-CIS is documented as seconds elapsed from an
arbitrary reference point (NOT a real calendar timestamp — there is no
public mapping to actual dates). We therefore derive cyclical/relative
time features from it, and explicitly do NOT invent a fake calendar date.

CRITICAL leakage rule enforced throughout this module:
    Every derived feature for row i must depend only on information with
    TransactionDT <= that row's own TransactionDT (or strictly < for
    "previous transaction" style features). No feature may look forward.
"""
from __future__ import annotations

import pandas as pd

from src.utils.logger import get_logger

logger = get_logger("temporal_features")

SECONDS_PER_HOUR = 3600
SECONDS_PER_DAY = 86400


def add_relative_time_features(df: pd.DataFrame, time_col: str) -> pd.DataFrame:
    """Derive hour-of-day / day-of-cycle features from the relative TransactionDT.

    These are safe by construction: they are a pure deterministic function
    of the transaction's OWN timestamp, so there is no leakage risk.
    """
    df = df.copy()
    df["tx_hour_of_day"] = (df[time_col] // SECONDS_PER_HOUR) % 24
    df["tx_day_of_cycle"] = (df[time_col] // SECONDS_PER_DAY) % 7
    df["tx_day_index"] = (df[time_col] // SECONDS_PER_DAY).astype(int)
    logger.info("Added tx_hour_of_day, tx_day_of_cycle, tx_day_index from %s", time_col)
    return df


def add_time_since_previous_transaction(
    df: pd.DataFrame, entity_col: str, time_col: str
) -> pd.DataFrame:
    """Time since this entity's previous transaction — leakage-safe by construction.

    Sorts by (entity, time), then takes a simple diff() within each entity
    group. Row i only ever looks at row i-1 (strictly earlier in time),
    never at anything in its own or a later row.
    """
    df = df.copy()
    df = df.sort_values([entity_col, time_col])
    df["time_since_prev_tx"] = (
        df.groupby(entity_col)[time_col].diff()
    )
    # First transaction per entity has no "previous" — NaN is correct here,
    # not an error to silently fill with 0 (0 would falsely imply "just did
    # another transaction a moment ago").
    logger.info(
        "Added time_since_prev_tx per %s (NaN for each entity's first "
        "observed transaction is expected and meaningful, not missing data).",
        entity_col,
    )
    return df


def chronological_split_indices(
    df: pd.DataFrame, time_col: str, train_frac: float, val_frac: float
) -> tuple[pd.Index, pd.Index, pd.Index]:
    """Return (train_idx, val_idx, test_idx) via a strict chronological split.

    This is the split strategy Phase 1 RQ3 (concept drift) requires: no
    shuffling, no random_state — training data is strictly earlier in time
    than validation, which is strictly earlier than test.
    """
    ordered = df.sort_values(time_col)
    n = len(ordered)
    train_end = int(n * train_frac)
    val_end = int(n * (train_frac + val_frac))

    train_idx = ordered.index[:train_end]
    val_idx = ordered.index[train_end:val_end]
    test_idx = ordered.index[val_end:]

    logger.info(
        "Chronological split -> train: %d rows (%s to %s), val: %d rows, test: %d rows",
        len(train_idx), ordered[time_col].iloc[0], ordered[time_col].iloc[train_end - 1],
        len(val_idx), len(test_idx),
    )
    return train_idx, val_idx, test_idx
