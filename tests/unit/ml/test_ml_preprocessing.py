"""Tests for leakage-safe tabular preprocessor — Phase 3."""
import pytest
import pandas as pd
import numpy as np

from src.ml.preprocessing import TabularPreprocessor


def test_preprocessor_fit_on_train_only():
    """Verify preprocessor fits statistics exclusively on X_train."""
    train_df = pd.DataFrame({
        "amt": [10.0, 20.0, 30.0, np.nan],  # median = 20.0
        "cat": ["A", "B", "A", "missing"],
    })

    test_df = pd.DataFrame({
        "amt": [100.0, np.nan],  # test missing should be imputed with train median (20.0)
        "cat": ["A", "C"],       # 'C' unseen in train
    })

    preprocessor = TabularPreprocessor(numeric_cols=["amt"], categorical_cols=["cat"], scale_numeric=False)
    preprocessor.fit(train_df)

    assert preprocessor.medians_["amt"] == 20.0

    X_test_trans = preprocessor.transform(test_df)
    assert X_test_trans["amt"].iloc[1] == 20.0
    assert f"amt_was_missing" in X_test_trans.columns
    assert X_test_trans["amt_was_missing"].iloc[1] == 1.0


def test_unseen_categories_handled_gracefully():
    """Verify unseen categories in test set do not crash transform."""
    train_df = pd.DataFrame({"cat": ["A", "B", "C", "A"]})
    test_df = pd.DataFrame({"cat": ["X", "Y"]})

    prep = TabularPreprocessor(categorical_cols=["cat"], scale_numeric=False)
    prep.fit(train_df)
    X_test = prep.transform(test_df)

    assert "cat_A" in X_test.columns
    assert X_test["cat_A"].sum() == 0.0
