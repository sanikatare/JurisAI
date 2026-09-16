"""SHAP Explainability Engine — Phase 4 Feature Attribution.

Computes exact or fallback SHAP (SHapley Additive exPlanations) values for individual transactions:
    - Identifies top positive risk-increasing features and negative risk-reducing features.
    - Formats output for inclusion in Evidence Bundles ([SHAP-001], [SHAP-002]).
"""
from __future__ import annotations

from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd

try:
    import shap
    HAS_SHAP = True
except ImportError:
    HAS_SHAP = False

from src.utils.logger import get_logger

logger = get_logger("shap_explainer")


class TransactionSHAPExplainer:
    """Computes SHAP feature attribution scores for transaction predictions."""

    def __init__(self, model: Any, feature_names: List[str]):
        """Initialize explainer.

        Args:
            model: Trained scikit-learn or XGBoost model.
            feature_names: List of input feature names.
        """
        self.model = model
        self.feature_names = feature_names
        self.explainer: Optional[Any] = None

        if HAS_SHAP:
            try:
                estimator = model
                if hasattr(model, "named_steps") and "model" in model.named_steps:
                    estimator = model.named_steps["model"]
                self.explainer = shap.TreeExplainer(estimator)
                logger.info("SHAP TreeExplainer initialized successfully.")
            except Exception as e:
                logger.warning("Could not initialize SHAP TreeExplainer (%s); using fallback attribution.", e)

    def explain_transaction(self, x_single: pd.DataFrame, top_k: int = 5) -> List[Dict[str, Any]]:
        """Explain a single transaction row and return top contributing features.

        Args:
            x_single: Single row DataFrame of preprocessed features.
            top_k: Number of top features to return.

        Returns:
            List of dictionaries containing feature name, SHAP contribution, and description.
        """
        if not isinstance(x_single, pd.DataFrame):
            x_single = pd.DataFrame(x_single, columns=self.feature_names)

        shap_values = None

        if HAS_SHAP and self.explainer is not None:
            try:
                raw_shap = self.explainer.shap_values(x_single)
                if isinstance(raw_shap, list):  # Binary classification list [class_0, class_1]
                    shap_values = raw_shap[1][0]
                elif isinstance(raw_shap, np.ndarray):
                    if raw_shap.ndim == 3:
                        shap_values = raw_shap[0, :, 1]
                    elif raw_shap.ndim == 2:
                        shap_values = raw_shap[0]
            except Exception as e:
                logger.warning("SHAP computation failed (%s); using fallback attribution.", e)

        # Fallback heuristic if SHAP library fails or is absent
        if shap_values is None:
            estimator = self.model
            if hasattr(self.model, "named_steps") and "model" in self.model.named_steps:
                estimator = self.model.named_steps["model"]

            if hasattr(estimator, "feature_importances_"):
                importances = estimator.feature_importances_
            else:
                importances = np.ones(len(self.feature_names)) / len(self.feature_names)

            row_vals = x_single.iloc[0].values
            # Heuristic attribution: importance * row_val
            shap_values = importances * (row_vals - np.mean(row_vals))

        # Sort by absolute magnitude
        abs_indices = np.argsort(np.abs(shap_values))[::-1][:top_k]

        explanations = []
        for idx in abs_indices:
            feat_name = self.feature_names[idx] if idx < len(self.feature_names) else f"feature_{idx}"
            contrib = float(shap_values[idx])
            feat_val = float(x_single.iloc[0, idx]) if idx < x_single.shape[1] else 0.0

            direction = "increased risk" if contrib > 0 else "reduced risk"
            explanations.append({
                "feature": feat_name,
                "feature_value": round(feat_val, 4),
                "shap_value": round(contrib, 4),
                "direction": direction,
                "formatted_attribution": f"{feat_name} = {feat_val:.2f} ({contrib:+.4f} {direction})"
            })

        return explanations
