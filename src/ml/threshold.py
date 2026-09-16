"""Threshold Analysis & Operating Point Selection — Phase 3 Section 6.

Performs systematic decision threshold sweeps over fraud probabilities:
    - Evaluates precision, recall, F1, FPR, FNR, and alert volume across thresholds.
    - Identifies optimal F1 operating point and fixed-FPR operating points.
    - Eliminates default 0.5 threshold assumption.
"""
from __future__ import annotations

from typing import Dict, Any, List
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score

from src.utils.logger import get_logger

logger = get_logger("ml_threshold")


def analyze_thresholds(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    steps: int = 100,
) -> pd.DataFrame:
    """Sweep classification thresholds and analyze operating trade-offs.

    Args:
        y_true: Ground truth binary labels.
        y_prob: Predicted fraud probabilities.
        steps: Number of threshold evaluation points between 0.01 and 0.99.

    Returns:
        DataFrame with columns [threshold, precision, recall, f1, fpr, fnr, num_alerts, alert_rate].
    """
    y_true = np.asarray(y_true).astype(int)
    y_prob = np.asarray(y_prob)
    thresholds = np.linspace(0.01, 0.99, steps)

    records = []
    total_samples = len(y_true)

    for thresh in thresholds:
        y_pred = (y_prob >= thresh).astype(int)
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()

        prec = float(tp / (tp + fp)) if (tp + fp) > 0 else 0.0
        rec = float(tp / (tp + fn)) if (tp + fn) > 0 else 0.0
        f1 = float(2 * prec * rec / (prec + rec)) if (prec + rec) > 0 else 0.0
        fpr = float(fp / (fp + tn)) if (fp + tn) > 0 else 0.0
        fnr = float(fn / (fn + tp)) if (fn + tp) > 0 else 0.0
        num_alerts = int(tp + fp)
        alert_rate = float(num_alerts / total_samples) if total_samples > 0 else 0.0

        records.append({
            "threshold": round(float(thresh), 4),
            "precision": round(prec, 5),
            "recall": round(rec, 5),
            "f1": round(f1, 5),
            "fpr": round(fpr, 5),
            "fnr": round(fnr, 5),
            "num_alerts": num_alerts,
            "alert_rate": round(alert_rate, 5),
            "tp": int(tp),
            "fp": int(fp),
            "tn": int(tn),
            "fn": int(fn),
        })

    threshold_df = pd.DataFrame(records)
    logger.info("Threshold sweep completed across %d operating points.", len(threshold_df))
    return threshold_df


def select_optimal_threshold(
    threshold_df: pd.DataFrame,
    criterion: str = "max_f1",
    target_fpr: float = 0.01,
) -> Dict[str, Any]:
    """Select decision threshold based on business or statistical criteria.

    Args:
        threshold_df: Output DataFrame from analyze_thresholds.
        criterion: "max_f1" or "fixed_fpr".
        target_fpr: Target FPR if criterion is "fixed_fpr".

    Returns:
        Dictionary detailing selected threshold and associated performance.
    """
    if threshold_df.empty:
        raise ValueError("Threshold DataFrame is empty.")

    if criterion == "max_f1":
        best_row = threshold_df.loc[threshold_df["f1"].idxmax()]
        reason = "Maximized F1 score"
    elif criterion == "fixed_fpr":
        valid_rows = threshold_df[threshold_df["fpr"] <= target_fpr]
        if not valid_rows.empty:
            best_row = valid_rows.loc[valid_rows["recall"].idxmax()]
            reason = f"Maximized Recall subject to FPR <= {target_fpr}"
        else:
            best_row = threshold_df.loc[threshold_df["fpr"].idxmin()]
            reason = f"Fallback to minimal FPR available"
    else:
        raise ValueError(f"Unknown threshold selection criterion: {criterion}")

    selected_info = {
        "selected_threshold": float(best_row["threshold"]),
        "selection_criterion": criterion,
        "selection_reason": reason,
        "f1": float(best_row["f1"]),
        "precision": float(best_row["precision"]),
        "recall": float(best_row["recall"]),
        "fpr": float(best_row["fpr"]),
        "fnr": float(best_row["fnr"]),
        "num_alerts": int(best_row["num_alerts"]),
        "alert_rate": float(best_row["alert_rate"]),
    }

    logger.info(
        "Threshold Selected (%s): Threshold=%.4f, F1=%.4f, Recall=%.4f, FPR=%.4f",
        criterion, selected_info["selected_threshold"], selected_info["f1"],
        selected_info["recall"], selected_info["fpr"]
    )
    return selected_info
