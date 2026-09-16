"""Tests for ML data splitting strategies — Phase 3."""
import pytest
import pandas as pd
import numpy as np

from src.ml.split import chronological_split, stratified_random_split


def test_chronological_split_ordering_and_no_overlap():
    """Verify chronological split maintains strict temporal order and zero index overlap."""
    np.random.seed(42)
    df = pd.DataFrame({
        "TransactionID": np.arange(100),
        "TransactionDT": np.sort(np.random.randint(1000, 5000, size=100)),
        "isFraud": np.random.choice([0, 1], size=100, p=[0.9, 0.1]),
    })

    train_df, val_df, test_df = chronological_split(
        df, time_col="TransactionDT", train_frac=0.6, val_frac=0.2, test_frac=0.2
    )

    # Check row counts
    assert len(train_df) == 60
    assert len(val_df) == 20
    assert len(test_df) == 20

    # Check zero overlap
    train_ids = set(train_df["TransactionID"])
    val_ids = set(val_df["TransactionID"])
    test_ids = set(test_df["TransactionID"])

    assert len(train_ids.intersection(val_ids)) == 0
    assert len(val_ids.intersection(test_ids)) == 0
    assert len(train_ids.intersection(test_ids)) == 0

    # Check strict temporal ordering
    assert train_df["TransactionDT"].max() <= val_df["TransactionDT"].min()
    assert val_df["TransactionDT"].max() <= test_df["TransactionDT"].min()


def test_stratified_random_split_proportions():
    """Verify stratified random split maintains target class ratios."""
    df = pd.DataFrame({
        "TransactionID": np.arange(200),
        "isFraud": [1] * 20 + [0] * 180,
    })

    train_df, val_df, test_df = stratified_random_split(
        df, target_col="isFraud", train_frac=0.6, val_frac=0.2, test_frac=0.2, random_seed=42
    )

    assert len(train_df) == 120
    assert len(val_df) == 40
    assert len(test_df) == 40

    # Stratified target ratio close to 0.10
    assert abs(train_df["isFraud"].mean() - 0.10) < 0.03
    assert abs(val_df["isFraud"].mean() - 0.10) < 0.03
    assert abs(test_df["isFraud"].mean() - 0.10) < 0.03
