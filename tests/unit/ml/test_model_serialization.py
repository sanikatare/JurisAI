"""Tests for joblib model artifact save/load contracts — Phase 3."""
import pytest
import os
import joblib
import pandas as pd
import numpy as np

from src.ml.train import train_model


def test_model_joblib_serialization(tmp_path):
    """Verify saved joblib model loads correctly and produces identical predictions."""
    X_train = pd.DataFrame(np.random.randn(50, 3), columns=["a", "b", "c"])
    y_train = pd.Series(np.random.choice([0, 1], size=50))

    model, meta = train_model(X_train, y_train, model_name="random_forest")
    prob_original = model.predict_proba(X_train)[:, 1]

    save_path = tmp_path / "rf_model.joblib"
    joblib.dump(model, save_path)

    loaded_model = joblib.load(save_path)
    prob_loaded = loaded_model.predict_proba(X_train)[:, 1]

    np.testing.assert_array_almost_equal(prob_original, prob_loaded)
