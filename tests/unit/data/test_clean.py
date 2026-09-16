"""Tests for src/data/clean.py using small synthetic fixtures.

These do NOT require the real IEEE-CIS dataset — they test the
transformation LOGIC in isolation, which is exactly what should be
testable before the real data is downloaded.
"""
import pandas as pd

from src.data.clean import clean

BASE_CONFIG = {
    "dataset": {
        "target_column": "isFraud",
        "id_column": "TransactionID",
        "time_column": "TransactionDT",
        "amount_column": "TransactionAmt",
    },
    "cleaning": {
        "missing_threshold_drop": 0.9,
        "high_cardinality_threshold": 100,
    },
}


def make_synthetic_df() -> pd.DataFrame:
    return pd.DataFrame({
        "TransactionID": [1, 2, 3, 4, 5],
        "isFraud": [0, 1, 0, 0, 1],
        "TransactionDT": [100, 200, 300, 400, 500],
        "TransactionAmt": [50.0, 200.0, 75.5, 10.0, 999.0],
        "ProductCD": ["W", "W", "C", "W", "R"],
        "fully_empty_col": [None, None, None, None, None],
        "constant_col": [1, 1, 1, 1, 1],
        "mostly_missing_col": [None, None, None, None, 5.0],  # 80% missing < 90% threshold, kept
        "partial_missing_numeric": [1.0, None, 3.0, None, 5.0],
        "partial_missing_categorical": ["a", None, "b", "a", None],
    })


def test_drops_fully_empty_and_constant_columns():
    df = make_synthetic_df()
    cleaned, log = clean(df, BASE_CONFIG, "isFraud")
    assert "fully_empty_col" not in cleaned.columns
    assert "constant_col" not in cleaned.columns
    actions = [s["action"] for s in log.steps]
    assert "drop_uninformative_columns" in actions


def test_never_drops_protected_columns_even_if_high_missing():
    df = make_synthetic_df()
    df["TransactionAmt"] = [None, None, None, None, 1.0]  # 80% missing, still protected
    cleaned, _ = clean(df, BASE_CONFIG, "isFraud")
    assert "TransactionAmt" in cleaned.columns
    assert "isFraud" in cleaned.columns
    assert "TransactionID" in cleaned.columns
    assert "TransactionDT" in cleaned.columns


def test_numeric_imputation_adds_missingness_indicator_not_blind_zero():
    df = make_synthetic_df()
    cleaned, _ = clean(df, BASE_CONFIG, "isFraud")
    assert "partial_missing_numeric_was_missing" in cleaned.columns
    # median of [1.0, 3.0, 5.0] = 3.0, NOT 0
    assert cleaned["partial_missing_numeric"].isna().sum() == 0
    imputed_rows = cleaned.loc[
        cleaned["partial_missing_numeric_was_missing"] == 1, "partial_missing_numeric"
    ]
    assert (imputed_rows == 3.0).all()


def test_categorical_imputation_uses_explicit_category_not_blind_fill():
    df = make_synthetic_df()
    cleaned, _ = clean(df, BASE_CONFIG, "isFraud")
    assert cleaned["partial_missing_categorical"].isna().sum() == 0
    assert "missing" in cleaned["partial_missing_categorical"].values


def test_duplicate_rows_are_flagged_not_silently_dropped():
    df = make_synthetic_df()
    dup_row = df.iloc[[0]].copy()
    df_with_dup = pd.concat([df, dup_row], ignore_index=True)
    cleaned, log = clean(df_with_dup, BASE_CONFIG, "isFraud")
    # Row count should be UNCHANGED (duplicates retained, only flagged)
    assert len(cleaned) == len(df_with_dup)
    actions = [s["action"] for s in log.steps]
    assert "flag_duplicate_rows" in actions
