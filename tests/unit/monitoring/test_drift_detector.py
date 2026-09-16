"""Tests for Population Stability Index (PSI) Data Drift Detector — Phase 5."""
import pytest
import numpy as np
import pandas as pd

from src.monitoring.drift_detector import DataDriftDetector


def test_drift_detector_evaluates_psi():
    """Verify DataDriftDetector calculates PSI and classifies status."""
    np.random.seed(42)
    df_baseline = pd.DataFrame({"amt": np.random.normal(100, 10, 500)})
    df_current_normal = np.random.normal(100, 10, 200)
    df_current_drifted = np.random.normal(250, 50, 200)

    detector = DataDriftDetector()
    detector.set_baseline(df_baseline, features=["amt"])

    res_normal = detector.evaluate_feature_drift("amt", df_current_normal)
    assert res_normal["status"] == "NORMAL"

    res_drifted = detector.evaluate_feature_drift("amt", df_current_drifted)
    assert res_drifted["status"] == "DRIFT"
    assert res_drifted["psi_score"] >= 0.25
