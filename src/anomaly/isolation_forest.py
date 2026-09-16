"""Unsupervised Anomaly Detection & Fusion — Phase 3 Section 11 (Experiment 3).

Implements Isolation Forest unsupervised novelty detection:
    - Trained strictly WITHOUT fraud labels.
    - Generates normalized anomaly scores [0.0, 1.0] where higher represents greater anomaly.
    - Evaluates model performance under Supervised Alone, Anomaly Alone, and Supervised + Anomaly Fusion.
"""
from __future__ import annotations

from typing import Dict, Any, Tuple, Optional
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

from src.utils.logger import get_logger

logger = get_logger("anomaly_isolation_forest")


class AnomalyDetector:
    """Unsupervised Isolation Forest wrapper for transaction novelty scoring."""

    def __init__(
        self,
        n_estimators: int = 100,
        contamination: float = 0.035,
        random_state: int = 42,
        n_jobs: int = -1,
    ):
        self.n_estimators = n_estimators
        self.contamination = contamination
        self.random_state = random_state
        self.n_jobs = n_jobs
        self.model = IsolationForest(
            n_estimators=self.n_estimators,
            contamination=self.contamination,
            random_state=self.random_state,
            n_jobs=self.n_jobs,
        )
        self.is_fitted = False

    def fit(self, X_train: pd.DataFrame) -> AnomalyDetector:
        """Fit Isolation Forest on feature matrix X_train (WITHOUT Y LABELS).

        Args:
            X_train: Training feature matrix.
        """
        logger.info("Fitting IsolationForest on %d samples (unsupervised)...", len(X_train))
        self.model.fit(X_train)
        self.is_fitted = True
        return self

    def predict_anomaly_score(self, X: pd.DataFrame) -> np.ndarray:
        """Predict continuous anomaly score scaled in range [0.0, 1.0].

        Higher score = more anomalous.

        Args:
            X: Input feature matrix.

        Returns:
            Array of anomaly scores [0.0, 1.0].
        """
        if not self.is_fitted:
            raise ValueError("AnomalyDetector must be fit before calling predict_anomaly_score.")

        # raw decision_function: lower (negative) values indicate anomalies
        raw_scores = self.model.decision_function(X)
        # Invert so higher score = higher anomaly risk
        inverted_scores = -raw_scores

        # Normalize via min-max scaling
        min_val = np.min(inverted_scores)
        max_val = np.max(inverted_scores)
        if max_val > min_val:
            scaled_scores = (inverted_scores - min_val) / (max_val - min_val)
        else:
            scaled_scores = np.zeros_like(inverted_scores)

        return scaled_scores


def evaluate_anomaly_fusion(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    supervised_trainer_fn: Any,
) -> Dict[str, Any]:
    """Execute Experiment 3 Anomaly Fusion Ablation.

    Compares:
        1. Model A: Supervised ML Alone
        2. Model B: Anomaly Score Alone
        3. Model C: Supervised ML + Anomaly Score Feature

    Args:
        X_train: Training features.
        y_train: Training labels.
        X_test: Test features.
        y_test: Test labels.
        supervised_trainer_fn: Function mapping (X_tr, y_tr) -> trained model.

    Returns:
        Dictionary containing ablation results table and comparison metrics.
    """
    from src.ml.metrics import evaluate_predictions

    # 1. Train Unsupervised Anomaly Model
    anomaly_detector = AnomalyDetector()
    anomaly_detector.fit(X_train)

    train_anomaly_scores = anomaly_detector.predict_anomaly_score(X_train)
    test_anomaly_scores = anomaly_detector.predict_anomaly_score(X_test)

    # Model A: Supervised ML Alone
    model_a, _ = supervised_trainer_fn(X_train, y_train)
    if hasattr(model_a, "predict_proba"):
        prob_a = model_a.predict_proba(X_test)[:, 1]
    else:
        prob_a = model_a.predict(X_test)
    metrics_a = evaluate_predictions(y_test, prob_a)

    # Model B: Anomaly Score Alone
    metrics_b = evaluate_predictions(y_test, test_anomaly_scores)

    # Model C: Supervised ML + Anomaly Score Feature
    X_train_fused = X_train.copy()
    X_train_fused["anomaly_score"] = train_anomaly_scores

    X_test_fused = X_test.copy()
    X_test_fused["anomaly_score"] = test_anomaly_scores

    model_c, _ = supervised_trainer_fn(X_train_fused, y_train)
    if hasattr(model_c, "predict_proba"):
        prob_c = model_c.predict_proba(X_test_fused)[:, 1]
    else:
        prob_c = model_c.predict(X_test_fused)
    metrics_c = evaluate_predictions(y_test, prob_c)

    results = {
        "model_a_supervised_alone": metrics_a,
        "model_b_anomaly_alone": metrics_b,
        "model_c_supervised_plus_anomaly": metrics_c,
        "pr_auc_delta": round(metrics_c["pr_auc"] - metrics_a["pr_auc"], 5),
        "recall_at_1pct_fpr_delta": round(metrics_c["recall_at_1pct_fpr"] - metrics_a["recall_at_1pct_fpr"], 5),
    }

    logger.info(
        "Experiment 3 Anomaly Fusion Complete: Supervised PR-AUC=%.4f, Anomaly Alone PR-AUC=%.4f, Fused PR-AUC=%.4f (Delta=%.4f)",
        metrics_a["pr_auc"], metrics_b["pr_auc"], metrics_c["pr_auc"], results["pr_auc_delta"]
    )

    return results
