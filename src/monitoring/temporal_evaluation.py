"""Temporal Performance & Concept Drift Monitoring — Phase 3 Section 20.

Evaluates model stability across chronological time windows:
    - Measures PR-AUC, Recall, F1, FPR, and Fraud Rate per temporal window.
    - Computes Population Stability Index (PSI) for numerical features across windows.
    - Generates temporal performance monitoring outputs for Power BI / PostgreSQL.
"""
from __future__ import annotations

from typing import Dict, Any, List
import numpy as np
import pandas as pd

from src.utils.logger import get_logger

logger = get_logger("temporal_evaluation")


def calculate_psi(
    reference: np.ndarray,
    target: np.ndarray,
    num_buckets: int = 10,
    eps: float = 1e-4,
) -> float:
    """Calculate Population Stability Index (PSI) between reference and target distributions.

    PSI < 0.1: No significant distribution change.
    0.1 <= PSI < 0.25: Moderate distribution shift.
    PSI >= 0.25: Significant concept / population drift.

    Args:
        reference: Reference feature values (e.g. training set).
        target: Target feature values (e.g. current temporal window).
        num_buckets: Quantile bucket count.
        eps: Small epsilon to prevent zero division.

    Returns:
        PSI scalar value.
    """
    reference = np.asarray(reference).astype(float)
    target = np.asarray(target).astype(float)

    reference = reference[~np.isnan(reference)]
    target = target[~np.isnan(target)]

    if len(reference) == 0 or len(target) == 0:
        return 0.0

    percentiles = np.linspace(0, 100, num_buckets + 1)
    quantiles = np.percentile(reference, percentiles)
    quantiles[0] -= 1e-5
    quantiles[-1] += 1e-5

    ref_counts, _ = np.histogram(reference, bins=quantiles)
    tgt_counts, _ = np.histogram(target, bins=quantiles)

    ref_pct = (ref_counts / len(reference)) + eps
    tgt_pct = (tgt_counts / len(target)) + eps

    psi_val = np.sum((tgt_pct - ref_pct) * np.log(tgt_pct / ref_pct))
    return float(psi_val)


def evaluate_temporal_performance(
    df_test: pd.DataFrame,
    y_true: np.ndarray,
    y_prob: np.ndarray,
    num_windows: int = 3,
    time_col: str = "TransactionDT",
    threshold: float = 0.5,
) -> pd.DataFrame:
    """Evaluate performance metrics broken down across chronological test windows.

    Args:
        df_test: Test DataFrame containing time_col.
        y_true: Ground truth binary labels.
        y_prob: Predicted fraud probabilities.
        num_windows: Number of equal chronological windows to slice test set into.
        time_col: Time column.
        threshold: Decision threshold.

    Returns:
        DataFrame containing window-level performance metrics.
    """
    from src.ml.metrics import evaluate_predictions

    df_test = df_test.copy()
    df_test["y_true"] = y_true
    df_test["y_prob"] = y_prob

    df_sorted = df_test.sort_values(time_col).reset_index(drop=True)
    window_size = int(np.ceil(len(df_sorted) / num_windows))

    records = []

    for w_idx in range(num_windows):
        start_idx = w_idx * window_size
        end_idx = min((w_idx + 1) * window_size, len(df_sorted))

        w_df = df_sorted.iloc[start_idx:end_idx]
        if w_df.empty:
            continue

        w_y_true = w_df["y_true"].values
        w_y_prob = w_df["y_prob"].values

        w_metrics = evaluate_predictions(w_y_true, w_y_prob, threshold=threshold)

        t_min = float(w_df[time_col].min())
        t_max = float(w_df[time_col].max())

        records.append({
            "window_index": w_idx + 1,
            "window_name": f"Window_{w_idx + 1}",
            "start_time": t_min,
            "end_time": t_max,
            "sample_count": len(w_df),
            "fraud_count": int(np.sum(w_y_true)),
            "fraud_rate": round(float(np.mean(w_y_true)), 5),
            "pr_auc": w_metrics["pr_auc"],
            "recall_at_1pct_fpr": w_metrics["recall_at_1pct_fpr"],
            "recall": w_metrics["recall"],
            "precision": w_metrics["precision"],
            "f1": w_metrics["f1"],
            "roc_auc": w_metrics["roc_auc"],
            "fpr": w_metrics["fpr"],
        })

    perf_df = pd.DataFrame(records)
    logger.info("Temporal performance evaluation completed across %d windows.", len(perf_df))
    return perf_df
