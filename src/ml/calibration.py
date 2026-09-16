"""Probability Calibration & Reliability Assessment — Phase 3 Section 17.

Evaluates raw predicted probabilities and fits probability calibrators:
    - Support for Platt Scaling (Logistic Regression on logits) and Isotonic Regression.
    - Evaluates calibration quality via Brier Score and calibration curves.
    - Ensures calibrator is fit on validation data and evaluated on holdout test data.
"""
from __future__ import annotations

from typing import Dict, Any, Tuple, Optional
import numpy as np
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV, calibration_curve
from sklearn.linear_model import LogisticRegression
from sklearn.isotonic import IsotonicRegression
from sklearn.metrics import brier_score_loss

from src.utils.logger import get_logger

logger = get_logger("ml_calibration")


class ProbabilityCalibrator:
    """Wrapper for probability calibration using Platt scaling or Isotonic regression."""

    def __init__(self, method: str = "platt"):
        """Initialize calibrator.

        Args:
            method: "platt" (sigmoid / logistic regression) or "isotonic".
        """
        if method not in ("platt", "isotonic"):
            raise ValueError("Method must be 'platt' or 'isotonic'")
        self.method = method
        self.model: Optional[Any] = None
        self.is_fitted: bool = False

    def fit(self, y_val_true: np.ndarray, y_val_prob: np.ndarray) -> ProbabilityCalibrator:
        """Fit calibration mapping strictly on validation probabilities.

        Args:
            y_val_true: Validation ground truth binary labels.
            y_val_prob: Validation raw uncalibrated probabilities.
        """
        y_val_true = np.asarray(y_val_true).astype(int)
        y_val_prob = np.asarray(y_val_prob).clip(1e-7, 1 - 1e-7)

        if self.method == "platt":
            # Logistic Regression on log-odds (logits)
            logits = np.log(y_val_prob / (1.0 - y_val_prob)).reshape(-1, 1)
            self.model = LogisticRegression(C=1e5, solver="lbfgs")
            self.model.fit(logits, y_val_true)
        else:
            # Isotonic Regression
            self.model = IsotonicRegression(out_of_bounds="clip")
            self.model.fit(y_val_prob, y_val_true)

        self.is_fitted = True
        logger.info("ProbabilityCalibrator (%s) fitted on %d validation samples.", self.method, len(y_val_true))
        return self

    def calibrate(self, y_prob: np.ndarray) -> np.ndarray:
        """Apply fitted calibration to raw probabilities.

        Args:
            y_prob: Raw probabilities.

        Returns:
            Calibrated probabilities bounded in [0.0, 1.0].
        """
        if not self.is_fitted or self.model is None:
            raise ValueError("Calibrator must be fit before calling calibrate.")

        y_prob = np.asarray(y_prob).clip(1e-7, 1 - 1e-7)

        if self.method == "platt":
            logits = np.log(y_prob / (1.0 - y_prob)).reshape(-1, 1)
            calibrated = self.model.predict_proba(logits)[:, 1]
        else:
            calibrated = self.model.predict(y_prob)

        return np.clip(calibrated, 0.0, 1.0)


def evaluate_calibration(
    y_true: np.ndarray,
    y_prob_raw: np.ndarray,
    y_prob_calibrated: np.ndarray,
    n_bins: int = 10,
) -> Dict[str, Any]:
    """Compute calibration metrics before and after calibration.

    Args:
        y_true: Ground truth binary labels.
        y_prob_raw: Raw uncalibrated probabilities.
        y_prob_calibrated: Calibrated probabilities.
        n_bins: Number of bins for reliability diagram computation.

    Returns:
        Dictionary containing Brier scores and calibration curve data.
    """
    y_true = np.asarray(y_true).astype(int)
    
    brier_raw = float(brier_score_loss(y_true, y_prob_raw))
    brier_calibrated = float(brier_score_loss(y_true, y_prob_calibrated))

    # Compute calibration curve points
    prob_true_raw, prob_pred_raw = calibration_curve(y_true, y_prob_raw, n_bins=n_bins, strategy="uniform")
    prob_true_cal, prob_pred_cal = calibration_curve(y_true, y_prob_calibrated, n_bins=n_bins, strategy="uniform")

    improvement_pct = ((brier_raw - brier_calibrated) / brier_raw * 100.0) if brier_raw > 0 else 0.0

    logger.info(
        "Probability Calibration Assessment: Raw Brier=%.5f, Calibrated Brier=%.5f (%.2f%% improvement)",
        brier_raw, brier_calibrated, improvement_pct
    )

    return {
        "brier_score_raw": round(brier_raw, 6),
        "brier_score_calibrated": round(brier_calibrated, 6),
        "brier_improvement_pct": round(improvement_pct, 2),
        "calibration_curve_raw": {
            "prob_true": [round(float(v), 5) for v in prob_true_raw],
            "prob_pred": [round(float(v), 5) for v in prob_pred_raw],
        },
        "calibration_curve_calibrated": {
            "prob_true": [round(float(v), 5) for v in prob_true_cal],
            "prob_pred": [round(float(v), 5) for v in prob_pred_cal],
        },
    }
