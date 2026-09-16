"""Model Monitoring & Alert Volume Logger — Phase 5 Part 20.

Tracks prediction volumes, alert rates, and risk-tier distributions.
"""
from __future__ import annotations

import datetime
from typing import Dict, Any, List
import pandas as pd
import numpy as np

from src.utils.logger import get_logger

logger = get_logger("model_monitor")


class ModelMonitor:
    """Tracks operational model health, prediction volume, and alert rates."""

    def __init__(self):
        self.predictions_history: List[Dict[str, Any]] = []

    def log_prediction(self, prediction_res: Dict[str, Any]):
        """Append real-time prediction output to monitoring memory log."""
        self.predictions_history.append(prediction_res)

    def compute_summary_metrics(self) -> Dict[str, Any]:
        """Compute window summary metrics over logged predictions."""
        if not self.predictions_history:
            return {
                "prediction_count": 0,
                "high_risk_count": 0,
                "medium_risk_count": 0,
                "low_risk_count": 0,
                "alert_rate": 0.0,
                "mean_calibrated_probability": 0.0,
            }

        df = pd.DataFrame(self.predictions_history)
        total = len(df)
        high = int((df["risk_tier"] == "High Risk").sum())
        medium = int((df["risk_tier"] == "Medium Risk").sum())
        low = int((df["risk_tier"] == "Low Risk").sum())

        mean_prob = float(df["calibrated_fraud_probability"].mean())
        alert_rate = float(high / total) if total > 0 else 0.0

        summary = {
            "prediction_count": total,
            "high_risk_count": high,
            "medium_risk_count": medium,
            "low_risk_count": low,
            "alert_rate": round(alert_rate, 4),
            "mean_calibrated_probability": round(mean_prob, 4),
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }

        logger.info("Model Monitoring Summary: Count=%d, HighRisk=%d, AlertRate=%.4f", total, high, alert_rate)
        return summary
