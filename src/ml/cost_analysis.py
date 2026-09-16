"""Business Cost & Expected Loss Analysis — Phase 3 Section 19.

Evaluates models under business cost matrices:
    - Fixed investigation cost per False Positive ($).
    - Fraud loss per False Negative (100% of transaction amount or multiplier).
    - Compares metric-optimized threshold vs financial-cost-optimized threshold.
"""
from __future__ import annotations

from typing import Dict, Any, List
import numpy as np
import pandas as pd

from src.utils.logger import get_logger

logger = get_logger("ml_cost_analysis")


def compute_expected_financial_loss(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    amounts: np.ndarray,
    threshold: float = 0.5,
    cost_fp: float = 15.0,
    fn_loss_multiplier: float = 1.0,
) -> Dict[str, Any]:
    """Calculate expected financial loss for a given decision threshold.

    Expected Loss = (FP_count * cost_fp) + sum(FN_amounts * fn_loss_multiplier)

    Args:
        y_true: Ground truth binary labels.
        y_prob: Fraud probabilities.
        amounts: Array of transaction dollar amounts.
        threshold: Decision threshold.
        cost_fp: Operational investigation cost per false positive ($).
        fn_loss_multiplier: Multiplier for fraud amount lost per false negative.

    Returns:
        Dictionary with cost breakdown.
    """
    y_true = np.asarray(y_true).astype(int)
    y_prob = np.asarray(y_prob)
    amounts = np.asarray(amounts).astype(float)
    y_pred = (y_prob >= threshold).astype(int)

    fp_mask = (y_true == 0) & (y_pred == 1)
    fn_mask = (y_true == 1) & (y_pred == 0)
    tp_mask = (y_true == 1) & (y_pred == 1)

    fp_count = int(np.sum(fp_mask))
    fn_count = int(np.sum(fn_mask))
    tp_count = int(np.sum(tp_mask))

    fp_total_cost = float(fp_count * cost_fp)
    fn_total_loss = float(np.sum(amounts[fn_mask]) * fn_loss_multiplier) if fn_count > 0 else 0.0
    prevented_fraud_amount = float(np.sum(amounts[tp_mask])) if tp_count > 0 else 0.0

    total_expected_loss = fp_total_cost + fn_total_loss

    return {
        "threshold": round(threshold, 4),
        "fp_count": fp_count,
        "fn_count": fn_count,
        "tp_count": tp_count,
        "fp_operational_cost": round(fp_total_cost, 2),
        "fn_fraud_loss": round(fn_total_loss, 2),
        "total_expected_loss": round(total_expected_loss, 2),
        "prevented_fraud_amount": round(prevented_fraud_amount, 2),
    }


def find_cost_optimal_threshold(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    amounts: np.ndarray,
    cost_fp: float = 15.0,
    fn_loss_multiplier: float = 1.0,
    steps: int = 100,
) -> Dict[str, Any]:
    """Sweep thresholds to locate the minimum expected financial loss operating point.

    Args:
        y_true: Ground truth binary labels.
        y_prob: Fraud probabilities.
        amounts: Array of transaction dollar amounts.
        cost_fp: Operational investigation cost per false positive ($).
        fn_loss_multiplier: Multiplier for fraud amount lost per false negative.
        steps: Number of threshold steps to evaluate.

    Returns:
        Dictionary with cost-optimal threshold details and comparison table.
    """
    thresholds = np.linspace(0.01, 0.99, steps)
    cost_sweep = []

    for thresh in thresholds:
        res = compute_expected_financial_loss(
            y_true, y_prob, amounts, threshold=thresh, cost_fp=cost_fp, fn_loss_multiplier=fn_loss_multiplier
        )
        cost_sweep.append(res)

    sweep_df = pd.DataFrame(cost_sweep)
    best_idx = sweep_df["total_expected_loss"].idxmin()
    best_row = sweep_df.loc[best_idx]

    logger.info(
        "Cost-Optimal Threshold Found: Threshold=%.4f, Total Loss=$%.2f (FP Cost=$%.2f, FN Loss=$%.2f)",
        best_row["threshold"], best_row["total_expected_loss"],
        best_row["fp_operational_cost"], best_row["fn_fraud_loss"]
    )

    return {
        "cost_optimal_threshold": float(best_row["threshold"]),
        "min_expected_loss": float(best_row["total_expected_loss"]),
        "fp_operational_cost": float(best_row["fp_operational_cost"]),
        "fn_fraud_loss": float(best_row["fn_fraud_loss"]),
        "prevented_fraud_amount": float(best_row["prevented_fraud_amount"]),
        "sweep_dataframe": sweep_df,
    }
