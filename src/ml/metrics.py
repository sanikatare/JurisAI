"""Standardized Evaluation Metrics for Fraud Detection — Phase 3 Section 5.

Implements consistent ML evaluation metrics:
    - Primary: PR-AUC (Precision-Recall AUC), Recall @ fixed FPR (1%, 5%), F1, Precision, Recall
    - Secondary: ROC-AUC, FPR, FNR, Confusion Matrix, Inference Latency
"""
from __future__ import annotations

import time
from typing import Dict, Any, Tuple, Optional
import numpy as np
from sklearn.metrics import (
    precision_recall_curve,
    auc,
    average_precision_score,
    roc_auc_score,
    roc_curve,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
)

from src.utils.logger import get_logger

logger = get_logger("ml_metrics")


def compute_recall_at_fixed_fpr(
    y_true: np.ndarray, y_prob: np.ndarray, target_fpr: float = 0.01
) -> Tuple[float, float]:
    """Compute Recall at a fixed False Positive Rate operating point.

    Args:
        y_true: Ground truth binary labels.
        y_prob: Predicted probability of fraud.
        target_fpr: Target False Positive Rate (e.g. 0.01 for 1% FPR).

    Returns:
        (achieved_recall, operating_threshold) tuple.
    """
    fpr, tpr, thresholds = roc_curve(y_true, y_prob)

    # Find closest threshold where FPR <= target_fpr
    valid_idx = np.where(fpr <= target_fpr)[0]
    if len(valid_idx) == 0:
        return 0.0, 1.0

    idx = valid_idx[-1]
    achieved_recall = float(tpr[idx])
    threshold = float(thresholds[idx]) if idx < len(thresholds) else 0.5
    return achieved_recall, threshold


def evaluate_predictions(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    threshold: float = 0.5,
    inference_time_sec: Optional[float] = None,
) -> Dict[str, Any]:
    """Compute standardized evaluation metrics dictionary.

    Args:
        y_true: Ground truth binary labels (0 or 1).
        y_prob: Predicted fraud probabilities [0, 1].
        threshold: Classification decision threshold (default 0.5).
        inference_time_sec: Total inference execution time in seconds (optional).

    Returns:
        Dictionary containing all primary, secondary, and confusion metrics.
    """
    y_true = np.asarray(y_true).astype(int)
    y_prob = np.asarray(y_prob)
    y_pred = (y_prob >= threshold).astype(int)

    # 1. Primary Metrics
    pr_auc = float(average_precision_score(y_true, y_prob))
    precision = float(precision_score(y_true, y_pred, zero_division=0))
    recall = float(recall_score(y_true, y_pred, zero_division=0))
    f1 = float(f1_score(y_true, y_pred, zero_division=0))

    # Recall at fixed FPR operating points
    recall_at_1pct_fpr, thresh_1pct = compute_recall_at_fixed_fpr(y_true, y_prob, target_fpr=0.01)
    recall_at_5pct_fpr, thresh_5pct = compute_recall_at_fixed_fpr(y_true, y_prob, target_fpr=0.05)

    # 2. Secondary Metrics
    try:
        roc_auc = float(roc_auc_score(y_true, y_prob))
    except ValueError:
        roc_auc = 0.5  # single class fallback

    cm = confusion_matrix(y_true, y_pred, labels=[0, 1])
    tn, fp, fn, tp = cm.ravel()

    fpr = float(fp / (fp + tn)) if (fp + tn) > 0 else 0.0
    fnr = float(fn / (fn + tp)) if (fn + tp) > 0 else 0.0

    latency_ms_per_sample = (
        (inference_time_sec * 1000.0 / len(y_true))
        if inference_time_sec is not None and len(y_true) > 0
        else 0.0
    )

    metrics = {
        "pr_auc": round(pr_auc, 5),
        "recall_at_1pct_fpr": round(recall_at_1pct_fpr, 5),
        "recall_at_5pct_fpr": round(recall_at_5pct_fpr, 5),
        "threshold_1pct_fpr": round(thresh_1pct, 5),
        "threshold_5pct_fpr": round(thresh_5pct, 5),
        "precision": round(precision, 5),
        "recall": round(recall, 5),
        "f1": round(f1, 5),
        "roc_auc": round(roc_auc, 5),
        "fpr": round(fpr, 5),
        "fnr": round(fnr, 5),
        "decision_threshold": round(threshold, 5),
        "confusion_matrix": {
            "tn": int(tn),
            "fp": int(fp),
            "fn": int(fn),
            "tp": int(tp),
        },
        "sample_count": len(y_true),
        "positive_count": int(np.sum(y_true)),
        "inference_latency_ms_per_sample": round(latency_ms_per_sample, 5),
    }

    return metrics
