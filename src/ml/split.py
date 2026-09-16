"""Data splitting strategies for ML model evaluation — Phase 3 Section 4.

Provides strict chronological splitting (primary for drift-aware evaluation)
and stratified random splitting (for baseline comparability).
Enforces zero overlap and temporal ordering validation.
"""
from __future__ import annotations

from typing import Tuple
import pandas as pd
from sklearn.model_selection import train_test_split

from src.utils.logger import get_logger

logger = get_logger("ml_split")


def chronological_split(
    df: pd.DataFrame,
    time_col: str = "TransactionDT",
    train_frac: float = 0.60,
    val_frac: float = 0.20,
    test_frac: float = 0.20,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Strict chronological split preserving TRAIN < VALIDATION < TEST timeline.

    Args:
        df: Input DataFrame containing time_col.
        time_col: Column name representing chronological order.
        train_frac: Proportion for training set.
        val_frac: Proportion for validation set.
        test_frac: Proportion for test set.

    Returns:
        (train_df, val_df, test_df) tuple.
    """
    if abs((train_frac + val_frac + test_frac) - 1.0) > 1e-5:
        raise ValueError("Split fractions must sum to 1.0")

    sorted_df = df.sort_values(time_col).reset_index(drop=True)
    n = len(sorted_df)

    train_end = int(n * train_frac)
    val_end = int(n * (train_frac + val_frac))

    train_df = sorted_df.iloc[:train_end].copy()
    val_df = sorted_df.iloc[train_end:val_end].copy()
    test_df = sorted_df.iloc[val_end:].copy()

    # Validation checks
    train_max_time = train_df[time_col].max() if not train_df.empty else 0
    val_min_time = val_df[time_col].min() if not val_df.empty else 0
    val_max_time = val_df[time_col].max() if not val_df.empty else 0
    test_min_time = test_df[time_col].min() if not test_df.empty else 0

    if not val_df.empty and train_max_time > val_min_time:
        logger.warning(
            "Temporal overlap warning: train_max_time (%s) > val_min_time (%s)",
            train_max_time, val_min_time
        )

    if not test_df.empty and val_max_time > test_min_time:
        logger.warning(
            "Temporal overlap warning: val_max_time (%s) > test_min_time (%s)",
            val_max_time, test_min_time
        )

    logger.info(
        "Chronological Split complete: Train=%d, Val=%d, Test=%d (Time ranges: Train [%s, %s], Val [%s, %s], Test [%s, %s])",
        len(train_df), len(val_df), len(test_df),
        train_df[time_col].min(), train_max_time,
        val_min_time, val_max_time,
        test_min_time, test_df[time_col].max()
    )

    return train_df, val_df, test_df


def stratified_random_split(
    df: pd.DataFrame,
    target_col: str = "isFraud",
    train_frac: float = 0.60,
    val_frac: float = 0.20,
    test_frac: float = 0.20,
    random_seed: int = 42,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Stratified random split for baseline comparative evaluation.

    Args:
        df: Input DataFrame.
        target_col: Column name for target stratification.
        train_frac: Training fraction.
        val_frac: Validation fraction.
        test_frac: Test fraction.
        random_seed: Random seed for reproducibility.

    Returns:
        (train_df, val_df, test_df) tuple.
    """
    if abs((train_frac + val_frac + test_frac) - 1.0) > 1e-5:
        raise ValueError("Split fractions must sum to 1.0")

    val_test_frac = val_frac + test_frac
    test_ratio = test_frac / val_test_frac

    train_df, val_test_df = train_test_split(
        df,
        test_size=val_test_frac,
        stratify=df[target_col] if target_col in df.columns else None,
        random_state=random_seed,
    )

    val_df, test_df = train_test_split(
        val_test_df,
        test_size=test_ratio,
        stratify=val_test_df[target_col] if target_col in val_test_df.columns else None,
        random_state=random_seed,
    )

    logger.info(
        "Stratified Random Split complete: Train=%d, Val=%d, Test=%d (Target positive rate: Train=%.4f, Val=%.4f, Test=%.4f)",
        len(train_df), len(val_df), len(test_df),
        train_df[target_col].mean() if target_col in train_df.columns else 0.0,
        val_df[target_col].mean() if target_col in val_df.columns else 0.0,
        test_df[target_col].mean() if target_col in test_df.columns else 0.0,
    )

    return train_df.copy(), val_df.copy(), test_df.copy()
