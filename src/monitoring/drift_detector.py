"""Real-Time Data Drift Detector — Phase 5 Part 21.

Calculates Population Stability Index (PSI) to detect feature distribution drift:
    - PSI < 0.10: NORMAL
    - 0.10 <= PSI < 0.25: WARNING
    - PSI >= 0.25: DRIFT
"""
from __future__ import annotations

import datetime
from typing import Dict, Any, List, Tuple
import numpy as np
import pandas as pd

from src.monitoring.temporal_evaluation import calculate_psi
from src.config import settings
from src.utils.logger import get_logger

logger = get_logger("drift_detector")


class DataDriftDetector:
    """Detects population stability drift across production features."""

    def __init__(
        self,
        warning_threshold: float = 0.10,
        alert_threshold: float = 0.25,
    ):
        self.warning_threshold = warning_threshold
        self.alert_threshold = alert_threshold
        self.baseline_data: Dict[str, np.ndarray] = {}

    def set_baseline(self, df_baseline: pd.DataFrame, features: Optional[List[str]] = None):
        """Set reference baseline distribution from training dataset."""
        features = features or list(df_baseline.select_dtypes(include=[np.number]).columns)
        for f in features:
            if f in df_baseline.columns:
                self.baseline_data[f] = df_baseline[f].dropna().values.astype(float)
        logger.info("Baseline distributions set for %d numerical features.", len(self.baseline_data))

    def evaluate_feature_drift(self, feature_name: str, current_values: np.ndarray) -> Dict[str, Any]:
        """Compute PSI and classify drift status for a single feature.

        Args:
            feature_name: Feature name.
            current_values: Array of current production feature values.

        Returns:
            Dictionary detailing feature drift metrics.
        """
        ref_vals = self.baseline_data.get(feature_name)
        if ref_vals is None or len(ref_vals) == 0 or len(current_values) == 0:
            return {
                "feature": feature_name,
                "psi_score": 0.0,
                "status": "NORMAL",
                "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            }

        psi_score = calculate_psi(ref_vals, current_values, num_buckets=10)

        if psi_score >= self.alert_threshold:
            status = "DRIFT"
        elif psi_score >= self.warning_threshold:
            status = "WARNING"
        else:
            status = "NORMAL"

        logger.info("Feature Drift Evaluated [%s]: PSI=%.4f (Status=%s)", feature_name, psi_score, status)

        return {
            "feature": feature_name,
            "baseline_sample_count": len(ref_vals),
            "current_sample_count": len(current_values),
            "psi_score": round(psi_score, 5),
            "status": status,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }
