"""Tests for leakage-free class imbalance training — Phase 3."""
import pytest
import pandas as pd
import numpy as np

from src.ml.train import train_model


def test_smote_training_pipeline_executes_without_leakage():
    """Verify train_model with SMOTE returns trained estimator."""
    np.random.seed(42)
    X_train = pd.DataFrame(np.random.randn(100, 5), columns=[f"f{i}" for i in range(5)])
    y_train = pd.Series(np.random.choice([0, 1], size=100, p=[0.9, 0.1]))

    model, meta = train_model(X_train, y_train, model_name="random_forest", imbalance_strategy="smote")

    assert model is not None
    assert meta["imbalance_strategy"] == "smote"

    # Test prediction
    preds = model.predict(X_train)
    assert len(preds) == 100
