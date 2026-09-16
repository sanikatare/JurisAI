"""Tests for metrics computation and probability calibration — Phase 3."""
import pytest
import numpy as np

from src.ml.metrics import evaluate_predictions, compute_recall_at_fixed_fpr
from src.ml.calibration import ProbabilityCalibrator, evaluate_calibration
from src.ml.threshold import analyze_thresholds, select_optimal_threshold


def test_evaluate_predictions_returns_valid_metrics():
    """Verify metrics calculator outputs all primary and secondary metrics."""
    y_true = np.array([0, 0, 0, 0, 1, 1, 1, 1])
    y_prob = np.array([0.1, 0.2, 0.3, 0.8, 0.2, 0.7, 0.9, 0.95])

    metrics = evaluate_predictions(y_true, y_prob, threshold=0.5)

    assert "pr_auc" in metrics
    assert "recall_at_1pct_fpr" in metrics
    assert "recall_at_5pct_fpr" in metrics
    assert "f1" in metrics
    assert "roc_auc" in metrics
    assert "confusion_matrix" in metrics


def test_probability_calibrator_platt():
    """Verify Platt scaling calibrates validation probabilities."""
    y_val_true = np.array([0, 0, 0, 0, 1, 1, 1, 1])
    y_val_prob = np.array([0.05, 0.1, 0.15, 0.7, 0.3, 0.8, 0.85, 0.9])

    calibrator = ProbabilityCalibrator(method="platt")
    calibrator.fit(y_val_true, y_val_prob)

    calibrated_probs = calibrator.calibrate(y_val_prob)

    assert len(calibrated_probs) == 8
    assert np.min(calibrated_probs) >= 0.0
    assert np.max(calibrated_probs) <= 1.0


def test_threshold_selection_max_f1():
    """Verify select_optimal_threshold returns max F1 threshold."""
    y_true = np.array([0, 0, 0, 1, 1, 1])
    y_prob = np.array([0.1, 0.2, 0.4, 0.6, 0.8, 0.9])

    thresh_df = analyze_thresholds(y_true, y_prob, steps=20)
    opt = select_optimal_threshold(thresh_df, criterion="max_f1")

    assert "selected_threshold" in opt
    assert opt["f1"] > 0.0
