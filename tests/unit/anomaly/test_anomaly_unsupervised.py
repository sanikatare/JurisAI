"""Tests for unsupervised anomaly detector — Phase 3."""
import pytest
import pandas as pd
import numpy as np

from src.anomaly.isolation_forest import AnomalyDetector, evaluate_anomaly_fusion
from src.ml.train import train_model


def test_isolation_forest_fits_without_target():
    """Verify AnomalyDetector fits on feature matrix without consuming y labels."""
    X_train = pd.DataFrame(np.random.randn(80, 4), columns=["f1", "f2", "f3", "f4"])

    detector = AnomalyDetector(n_estimators=10)
    detector.fit(X_train)

    scores = detector.predict_anomaly_score(X_train)

    assert len(scores) == 80
    assert np.min(scores) >= 0.0
    assert np.max(scores) <= 1.0


def test_anomaly_fusion_ablation_runs():
    """Verify evaluate_anomaly_fusion executes all 3 ablation branches."""
    X_train = pd.DataFrame(np.random.randn(80, 4), columns=["f1", "f2", "f3", "f4"])
    y_train = pd.Series(np.random.choice([0, 1], size=80, p=[0.85, 0.15]))
    X_test = pd.DataFrame(np.random.randn(40, 4), columns=["f1", "f2", "f3", "f4"])
    y_test = pd.Series(np.random.choice([0, 1], size=40, p=[0.85, 0.15]))

    def trainer(X_tr, y_tr):
        return train_model(X_tr, y_tr, model_name="logistic_regression")

    res = evaluate_anomaly_fusion(X_train, y_train, X_test, y_test, supervised_trainer_fn=trainer)

    assert "model_a_supervised_alone" in res
    assert "model_b_anomaly_alone" in res
    assert "model_c_supervised_plus_anomaly" in res
    assert "pr_auc_delta" in res
