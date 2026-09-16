"""Supervised ML Model Trainers — Phase 3 Section 5 & Section 7.

Trains baseline models (Logistic Regression, Random Forest, XGBoost / HistGradientBoosting)
with configurable class imbalance handling (Class Weighting, SMOTE in pipeline).
Strictly prevents leakage by fitting samplers and preprocessors on training data only.
"""
from __future__ import annotations

from typing import Dict, Any, Tuple, Optional
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier

try:
    import xgboost as xgb
    HAS_XGBOOST = True
except ImportError:
    HAS_XGBOOST = False

try:
    from imblearn.pipeline import Pipeline as ImbPipeline
    from imblearn.over_sampling import SMOTE
    HAS_IMBLEARN = True
except ImportError:
    HAS_IMBLEARN = False

from src.utils.logger import get_logger

logger = get_logger("ml_train")


def build_model_instance(
    model_name: str,
    imbalance_strategy: str = "none",
    random_seed: int = 42,
    params: Optional[Dict[str, Any]] = None,
) -> Any:
    """Instantiate classifier based on model_name and imbalance_strategy.

    Args:
        model_name: "logistic_regression", "random_forest", or "xgboost".
        imbalance_strategy: "none", "class_weight", or "smote".
        random_seed: Random seed.
        params: Custom hyperparameter overrides.

    Returns:
        Configured scikit-learn compatible classifier.
    """
    params = params or {}
    use_class_weight = (imbalance_strategy == "class_weight")

    if model_name == "logistic_regression":
        cw = "balanced" if use_class_weight else None
        model = LogisticRegression(
            max_iter=params.get("max_iter", 1000),
            C=params.get("C", 1.0),
            solver=params.get("solver", "lbfgs"),
            class_weight=cw,
            random_state=random_seed,
        )

    elif model_name == "random_forest":
        cw = "balanced" if use_class_weight else None
        model = RandomForestClassifier(
            n_estimators=params.get("n_estimators", 100),
            max_depth=params.get("max_depth", 12),
            min_samples_leaf=params.get("min_samples_leaf", 5),
            class_weight=cw,
            random_state=random_seed,
            n_jobs=params.get("n_jobs", -1),
        )

    elif model_name == "xgboost":
        if HAS_XGBOOST:
            scale_pos_weight = params.get("scale_pos_weight", 20.0) if use_class_weight else 1.0
            model = xgb.XGBClassifier(
                n_estimators=params.get("n_estimators", 100),
                max_depth=params.get("max_depth", 6),
                learning_rate=params.get("learning_rate", 0.1),
                subsample=params.get("subsample", 0.8),
                colsample_bytree=params.get("colsample_bytree", 0.8),
                scale_pos_weight=scale_pos_weight,
                random_state=random_seed,
                n_jobs=params.get("n_jobs", -1),
                eval_metric="logloss",
            )
        else:
            logger.warning("XGBoost not available; falling back to HistGradientBoostingClassifier")
            class_weight = "balanced" if use_class_weight else None
            model = HistGradientBoostingClassifier(
                max_iter=params.get("n_estimators", 100),
                max_depth=params.get("max_depth", 6),
                learning_rate=params.get("learning_rate", 0.1),
                class_weight=class_weight,
                random_state=random_seed,
            )
    else:
        raise ValueError(f"Unsupported model_name: {model_name}")

    return model


def train_model(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    model_name: str = "random_forest",
    imbalance_strategy: str = "none",
    random_seed: int = 42,
    params: Optional[Dict[str, Any]] = None,
) -> Tuple[Any, Dict[str, Any]]:
    """Train supervised ML model on preprocessed training data.

    Applies SMOTE strictly inside the pipeline if requested, guaranteeing zero test set contamination.

    Args:
        X_train: Training feature matrix.
        y_train: Training target labels.
        model_name: Model identifier.
        imbalance_strategy: "none", "class_weight", or "smote".
        random_seed: Random seed.
        params: Custom hyperparameter overrides.

    Returns:
        (fitted_model_or_pipeline, metadata_dict) tuple.
    """
    model = build_model_instance(
        model_name=model_name,
        imbalance_strategy=imbalance_strategy,
        random_seed=random_seed,
        params=params,
    )

    if imbalance_strategy == "smote":
        if HAS_IMBLEARN:
            smote = SMOTE(random_state=random_seed, k_neighbors=3)
            pipeline = ImbPipeline(steps=[("smote", smote), ("model", model)])
            logger.info("Training %s with SMOTE oversampling in ImbPipeline...", model_name)
            pipeline.fit(X_train, y_train)
            fitted_obj = pipeline
        else:
            logger.warning("imblearn not installed; falling back to SMOTE-free training with class_weight")
            model = build_model_instance(
                model_name=model_name,
                imbalance_strategy="class_weight",
                random_seed=random_seed,
                params=params,
            )
            model.fit(X_train, y_train)
            fitted_obj = model
    else:
        logger.info("Training %s (imbalance strategy: %s)...", model_name, imbalance_strategy)
        model.fit(X_train, y_train)
        fitted_obj = model

    metadata = {
        "model_name": model_name,
        "imbalance_strategy": imbalance_strategy,
        "random_seed": random_seed,
        "n_train_samples": len(X_train),
        "n_features": X_train.shape[1],
        "feature_names": list(X_train.columns),
    }

    return fitted_obj, metadata


def get_feature_importance(model_or_pipeline: Any, feature_names: list[str]) -> pd.DataFrame:
    """Extract feature importance array from fitted estimator.

    Args:
        model_or_pipeline: Fitted sklearn model or imblearn pipeline.
        feature_names: List of input feature names.

    Returns:
        DataFrame sorted by feature importance descending.
    """
    estimator = model_or_pipeline
    if hasattr(model_or_pipeline, "named_steps") and "model" in model_or_pipeline.named_steps:
        estimator = model_or_pipeline.named_steps["model"]

    importances = None
    if hasattr(estimator, "feature_importances_"):
        importances = estimator.feature_importances_
    elif hasattr(estimator, "coef_"):
        importances = np.abs(estimator.coef_[0])

    if importances is None or len(importances) != len(feature_names):
        importances = np.zeros(len(feature_names))

    imp_df = pd.DataFrame({
        "feature": feature_names,
        "importance": importances,
    }).sort_values("importance", ascending=False).reset_index(drop=True)

    return imp_df
