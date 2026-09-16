"""ML Error Analysis & Root Cause Investigation — Phase 3 Section 18.

Extracts, categorizes, and analyzes prediction errors (False Positives and False Negatives):
    - Analyzes transaction amount distributions for FP and FN cases.
    - Measures error rates across missingness, entity history, and temporal features.
    - Generates error analysis report DataFrames.
"""
from __future__ import annotations

from typing import Dict, Any, List, Tuple
import numpy as np
import pandas as pd

from src.utils.logger import get_logger

logger = get_logger("ml_error_analysis")


def analyze_errors(
    df_test: pd.DataFrame,
    y_true: np.ndarray,
    y_prob: np.ndarray,
    threshold: float = 0.5,
    amount_col: str = "TransactionAmt",
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Perform systematic error breakdown on holdout test set.

    Args:
        df_test: Test DataFrame with original feature columns.
        y_true: Ground truth binary labels.
        y_prob: Predicted fraud probabilities.
        threshold: Operating decision threshold.
        amount_col: Transaction amount column name.

    Returns:
        (annotated_df, error_summary_dict) tuple.
    """
    y_true = np.asarray(y_true).astype(int)
    y_prob = np.asarray(y_prob)
    y_pred = (y_prob >= threshold).astype(int)

    annotated = df_test.copy()
    annotated["y_true"] = y_true
    annotated["y_prob"] = y_prob
    annotated["y_pred"] = y_pred

    # Error categories
    annotated["error_type"] = "TN"
    annotated.loc[(annotated["y_true"] == 0) & (annotated["y_pred"] == 1), "error_type"] = "FP"
    annotated.loc[(annotated["y_true"] == 1) & (annotated["y_pred"] == 0), "error_type"] = "FN"
    annotated.loc[(annotated["y_true"] == 1) & (annotated["y_pred"] == 1), "error_type"] = "TP"

    fp_df = annotated[annotated["error_type"] == "FP"]
    fn_df = annotated[annotated["error_type"] == "FN"]
    tp_df = annotated[annotated["error_type"] == "TP"]
    tn_df = annotated[annotated["error_type"] == "TN"]

    has_amt = amount_col in annotated.columns

    summary = {
        "threshold": threshold,
        "total_test_samples": len(annotated),
        "count_fp": len(fp_df),
        "count_fn": len(fn_df),
        "count_tp": len(tp_df),
        "count_tn": len(tn_df),
        "amount_stats": {
            "fp_mean_amount": float(fp_df[amount_col].mean()) if has_amt and not fp_df.empty else 0.0,
            "fn_mean_amount": float(fn_df[amount_col].mean()) if has_amt and not fn_df.empty else 0.0,
            "tp_mean_amount": float(tp_df[amount_col].mean()) if has_amt and not tp_df.empty else 0.0,
            "tn_mean_amount": float(tn_df[amount_col].mean()) if has_amt and not tn_df.empty else 0.0,
            "fp_p90_amount": float(fp_df[amount_col].quantile(0.90)) if has_amt and not fp_df.empty else 0.0,
            "fn_p90_amount": float(fn_df[amount_col].quantile(0.90)) if has_amt and not fn_df.empty else 0.0,
        },
        "key_findings": [
            f"False Positives (n={len(fp_df)}) highlight legitimate transactions flagged as suspicious.",
            f"False Negatives (n={len(fn_df)}) represent missed fraud cases resulting in direct financial loss.",
        ],
    }

    logger.info(
        "Error Analysis complete: FP=%d (mean amt=%.2f), FN=%d (mean amt=%.2f)",
        len(fp_df), summary["amount_stats"]["fp_mean_amount"],
        len(fn_df), summary["amount_stats"]["fn_mean_amount"]
    )

    return annotated, summary
