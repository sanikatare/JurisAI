"""Tests specifically targeting the Phase 2 Part 20 requirement:
'no-future-data leakage in rolling features'.

These construct a small synthetic timeline where the correct leakage-safe
answer can be hand-computed, and assert the pipeline matches it exactly.
"""
import pandas as pd

from src.features.entity_features import add_entity_rolling_features
from src.features.temporal_features import (
    add_relative_time_features,
    add_time_since_previous_transaction,
    chronological_split_indices,
)


def test_relative_time_features_are_deterministic_per_row():
    df = pd.DataFrame({"TransactionDT": [0, 3600, 7200, 90000]})
    out = add_relative_time_features(df, "TransactionDT")
    assert out["tx_hour_of_day"].tolist() == [0, 1, 2, 1]  # 90000s = 25h -> hour 1 of next day


def test_time_since_previous_transaction_never_uses_future_rows():
    # entity A: transactions at t=0, 100, 250 ; entity B: t=50, 300
    df = pd.DataFrame({
        "entity": ["A", "B", "A", "A", "B"],
        "TransactionDT": [0, 50, 100, 250, 300],
    })
    out = add_time_since_previous_transaction(df, entity_col="entity", time_col="TransactionDT")
    out = out.set_index("TransactionDT")
    # A's first tx (t=0) has no prior -> NaN
    assert pd.isna(out.loc[0, "time_since_prev_tx"])
    # A's second tx (t=100) prior was t=0 -> diff = 100
    assert out.loc[100, "time_since_prev_tx"] == 100
    # A's third tx (t=250) prior was t=100 -> diff = 150
    assert out.loc[250, "time_since_prev_tx"] == 150
    # B's first tx (t=50) has no prior -> NaN
    assert pd.isna(out.loc[50, "time_since_prev_tx"])
    # B's second tx (t=300) prior was t=50 -> diff = 250
    assert out.loc[300, "time_since_prev_tx"] == 250


def test_entity_rolling_amount_mean_excludes_current_row():
    # entity A spends 10, then 20, then 30 -> prior_amount_mean before the
    # 3rd transaction must be mean(10, 20) = 15, NOT mean(10, 20, 30).
    df = pd.DataFrame({
        "entity": ["A", "A", "A"],
        "TransactionDT": [0, 100, 200],
        "TransactionAmt": [10.0, 20.0, 30.0],
    })
    out = add_entity_rolling_features(df, entity_col="entity", amount_col="TransactionAmt",
                                       time_col="TransactionDT")
    out = out.sort_values("TransactionDT").reset_index(drop=True)

    assert pd.isna(out.loc[0, "entity_prior_amount_mean"])          # no prior tx
    assert out.loc[1, "entity_prior_amount_mean"] == 10.0            # only the first tx precedes it
    assert out.loc[2, "entity_prior_amount_mean"] == 15.0            # mean(10, 20), NOT mean(10, 20, 30)

    assert out.loc[0, "entity_prior_tx_count"] == 0
    assert out.loc[1, "entity_prior_tx_count"] == 1
    assert out.loc[2, "entity_prior_tx_count"] == 2


def test_chronological_split_never_shuffles():
    df = pd.DataFrame({"TransactionDT": [500, 100, 300, 200, 400]})
    train_idx, val_idx, test_idx = chronological_split_indices(
        df, time_col="TransactionDT", train_frac=0.6, val_frac=0.2
    )
    train_times = df.loc[train_idx, "TransactionDT"].tolist()
    val_times = df.loc[val_idx, "TransactionDT"].tolist()
    test_times = df.loc[test_idx, "TransactionDT"].tolist()

    # Every train time must be <= every val time <= every test time.
    assert max(train_times) <= min(val_times)
    assert max(val_times) <= min(test_times)
