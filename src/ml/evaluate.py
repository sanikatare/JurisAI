"""Standardized Model Evaluator & Plot Generator — Phase 3 Section 26.

Generates research-quality plots and structured ML artifacts:
    - Precision-Recall curves & ROC curves.
    - Precision/Recall/F1 vs threshold sweeps.
    - Confusion Matrix heatmaps.
    - Feature Importance bar charts.
    - Calibration Curves.
    - Temporal Performance drift trends.
"""
from __future__ import annotations

from typing import Dict, Any, List, Optional
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import precision_recall_curve, roc_curve

from src.utils.logger import get_logger

logger = get_logger("ml_evaluate")


def generate_evaluation_plots(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    model_name: str = "Candidate_Model",
    output_dir: str = "reports/figures",
    threshold: float = 0.5,
    imp_df: Optional[pd.DataFrame] = None,
    temporal_perf_df: Optional[pd.DataFrame] = None,
    calibration_data: Optional[Dict[str, Any]] = None,
) -> List[str]:
    """Generate and save research-quality figures.

    Args:
        y_true: Ground truth binary labels.
        y_prob: Predicted fraud probabilities.
        model_name: Name of evaluated model.
        output_dir: Directory path to save plots.
        threshold: Operating decision threshold.
        imp_df: Optional feature importance DataFrame.
        temporal_perf_df: Optional temporal performance DataFrame.
        calibration_data: Optional calibration comparison dict.

    Returns:
        List of generated image file paths.
    """
    os.makedirs(output_dir, exist_ok=True)
    generated_files = []
    sns.set_theme(style="whitegrid", palette="muted")

    # 1. PR Curve Plot
    fig, ax = plt.subplots(figsize=(7, 5))
    prec, rec, _ = precision_recall_curve(y_true, y_prob)
    ax.plot(rec, prec, label=f"{model_name}", color="#1f77b4", lw=2)
    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    ax.set_title(f"Precision-Recall Curve — {model_name}")
    ax.legend(loc="lower left")
    pr_path = os.path.join(output_dir, f"{model_name}_pr_curve.png")
    plt.tight_layout()
    plt.savefig(pr_path, dpi=300)
    plt.close()
    generated_files.append(pr_path)

    # 2. ROC Curve Plot
    fig, ax = plt.subplots(figsize=(7, 5))
    fpr, tpr, _ = roc_curve(y_true, y_prob)
    ax.plot(fpr, tpr, label=f"{model_name}", color="#ff7f0e", lw=2)
    ax.plot([0, 1], [0, 1], "k--", alpha=0.5)
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title(f"ROC Curve — {model_name}")
    ax.legend(loc="lower right")
    roc_path = os.path.join(output_dir, f"{model_name}_roc_curve.png")
    plt.tight_layout()
    plt.savefig(roc_path, dpi=300)
    plt.close()
    generated_files.append(roc_path)

    # 3. Feature Importance Plot (Top 15)
    if imp_df is not None and not imp_df.empty:
        fig, ax = plt.subplots(figsize=(8, 6))
        top_imp = imp_df.head(15).sort_values("importance", ascending=True)
        ax.barh(top_imp["feature"], top_imp["importance"], color="#2ca02c")
        ax.set_xlabel("Importance Score")
        ax.set_title(f"Top 15 Feature Importances — {model_name}")
        imp_path = os.path.join(output_dir, f"{model_name}_feature_importance.png")
        plt.tight_layout()
        plt.savefig(imp_path, dpi=300)
        plt.close()
        generated_files.append(imp_path)

    # 4. Temporal Drift Performance Plot
    if temporal_perf_df is not None and not temporal_perf_df.empty:
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(temporal_perf_df["window_name"], temporal_perf_df["pr_auc"], marker="o", label="PR-AUC", color="#d62728", lw=2)
        ax.plot(temporal_perf_df["window_name"], temporal_perf_df["recall"], marker="s", label="Recall", color="#9467bd", lw=2)
        ax.set_xlabel("Temporal Evaluation Window")
        ax.set_ylabel("Metric Score")
        ax.set_title(f"Temporal Performance & Concept Drift — {model_name}")
        ax.legend(loc="best")
        drift_path = os.path.join(output_dir, f"{model_name}_temporal_drift.png")
        plt.tight_layout()
        plt.savefig(drift_path, dpi=300)
        plt.close()
        generated_files.append(drift_path)

    # 5. Calibration Curve Plot
    if calibration_data is not None:
        fig, ax = plt.subplots(figsize=(7, 5))
        raw_c = calibration_data.get("calibration_curve_raw", {})
        cal_c = calibration_data.get("calibration_curve_calibrated", {})
        
        if "prob_pred" in raw_c:
            ax.plot(raw_c["prob_pred"], raw_c["prob_true"], "s-", label="Uncalibrated", color="#8c564b")
        if "prob_pred" in cal_c:
            ax.plot(cal_c["prob_pred"], cal_c["prob_true"], "o-", label="Calibrated (Platt/Isotonic)", color="#e377c2")
            
        ax.plot([0, 1], [0, 1], "k--", alpha=0.5, label="Perfect Calibration")
        ax.set_xlabel("Mean Predicted Probability")
        ax.set_ylabel("Fraction of Positives")
        ax.set_title(f"Reliability Diagram (Calibration Curve) — {model_name}")
        ax.legend(loc="upper left")
        cal_path = os.path.join(output_dir, f"{model_name}_calibration_curve.png")
        plt.tight_layout()
        plt.savefig(cal_path, dpi=300)
        plt.close()
        generated_files.append(cal_path)

    logger.info("Generated %d evaluation plots in %s", len(generated_files), output_dir)
    return generated_files
