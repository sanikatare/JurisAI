"""Tabular Preprocessing Pipeline — Phase 3 Section 4 & Section 8.

Enforces strict leakage-free preprocessing:
    - Preprocessor is fit strictly on training data ONLY.
    - Numerical missingness imputed with median + explicit `_was_missing` indicator.
    - Categorical missingness filled with explicit "missing" category.
    - Categorical encoding via Frequency Encoding (for high cardinality) and One-Hot Encoding (low cardinality).
    - StandardScaler applied to numerical features.
"""
from __future__ import annotations

from typing import List, Dict, Tuple, Optional, Any
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler

from src.utils.logger import get_logger

logger = get_logger("ml_preprocessing")


class TabularPreprocessor(BaseEstimator, TransformerMixin):
    """Leakage-safe preprocessor for IEEE-CIS tabular features."""

    def __init__(
        self,
        numeric_cols: Optional[List[str]] = None,
        categorical_cols: Optional[List[str]] = None,
        high_cardinality_threshold: int = 50,
        scale_numeric: bool = True,
    ):
        self.numeric_cols = numeric_cols or []
        self.categorical_cols = categorical_cols or []
        self.high_cardinality_threshold = high_cardinality_threshold
        self.scale_numeric = scale_numeric

        # Fitted parameters
        self.medians_: Dict[str, float] = {}
        self.freq_encodings_: Dict[str, Dict[Any, float]] = {}
        self.onehot_categories_: Dict[str, List[Any]] = {}
        self.scaler_: Optional[StandardScaler] = None
        self.feature_names_out_: List[str] = []
        self.is_fitted_: bool = False

    def fit(self, X: pd.DataFrame, y: Optional[pd.Series] = None) -> TabularPreprocessor:
        """Fit preprocessing statistics strictly on X_train.

        Args:
            X: Training DataFrame (X_train).
            y: Target Series (unused during fitting to prevent target leakage).
        """
        X = X.copy()
        
        # Auto-detect column types if not provided
        if not self.numeric_cols and not self.categorical_cols:
            self.numeric_cols = list(X.select_dtypes(include=[np.number]).columns)
            self.categorical_cols = list(X.select_dtypes(exclude=[np.number]).columns)

        # 1. Compute medians for numerical columns
        for col in self.numeric_cols:
            if col in X.columns:
                self.medians_[col] = float(X[col].median() if not X[col].dropna().empty else 0.0)

        # 2. Compute encodings for categorical columns
        for col in self.categorical_cols:
            if col in X.columns:
                filled_series = X[col].astype(str).fillna("missing")
                unique_vals = filled_series.unique()
                if len(unique_vals) > self.high_cardinality_threshold:
                    # Frequency encoding based strictly on train frequencies
                    counts = filled_series.value_counts(normalize=True).to_dict()
                    self.freq_encodings_[col] = counts
                else:
                    # One-hot categories
                    self.onehot_categories_[col] = list(unique_vals)

        # Build feature names list after transformation schema
        output_features = []
        for col in self.numeric_cols:
            if col in X.columns:
                output_features.append(col)
                # missingness indicator if column had NaNs in train
                if X[col].isna().any():
                    output_features.append(f"{col}_was_missing")

        for col in self.categorical_cols:
            if col in X.columns:
                if col in self.freq_encodings_:
                    output_features.append(f"{col}_freq")
                elif col in self.onehot_categories_:
                    for cat in self.onehot_categories_[col]:
                        output_features.append(f"{col}_{cat}")

        self.feature_names_out_ = output_features

        # 3. Fit scaler if requested
        if self.scale_numeric and self.numeric_cols:
            X_num_imputed = self._impute_numeric(X)
            self.scaler_ = StandardScaler()
            self.scaler_.fit(X_num_imputed)

        self.is_fitted_ = True
        logger.info(
            "TabularPreprocessor fitted successfully: %d numeric cols, %d categorical cols -> %d output features.",
            len(self.numeric_cols), len(self.categorical_cols), len(self.feature_names_out_)
        )
        return self

    def _impute_numeric(self, X: pd.DataFrame) -> pd.DataFrame:
        """Internal helper to impute numeric columns."""
        num_df = pd.DataFrame(index=X.index)
        for col in self.numeric_cols:
            if col in X.columns:
                median_val = self.medians_.get(col, 0.0)
                num_df[col] = X[col].fillna(median_val)
        return num_df

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Transform input DataFrame using parameters fit on training data."""
        if not self.is_fitted_:
            raise ValueError("TabularPreprocessor must be fit before transform.")

        X = X.copy()
        transformed_parts = []

        # 1. Transform Numeric Columns + Missing Indicators
        num_df = pd.DataFrame(index=X.index)
        for col in self.numeric_cols:
            if col in X.columns:
                median_val = self.medians_.get(col, 0.0)
                # Was missing indicator
                if f"{col}_was_missing" in self.feature_names_out_:
                    num_df[f"{col}_was_missing"] = X[col].isna().astype(float)
                num_df[col] = X[col].fillna(median_val)
            else:
                num_df[col] = 0.0

        if self.scale_numeric and self.scaler_ is not None:
            # Scale numeric features (excluding missing indicators)
            num_cols_to_scale = [c for c in self.numeric_cols if c in num_df.columns]
            num_df[num_cols_to_scale] = self.scaler_.transform(num_df[num_cols_to_scale])

        transformed_parts.append(num_df)

        # 2. Transform Categorical Columns
        cat_df = pd.DataFrame(index=X.index)
        for col in self.categorical_cols:
            if col in X.columns:
                filled_series = X[col].astype(str).fillna("missing")
                if col in self.freq_encodings_:
                    freq_map = self.freq_encodings_[col]
                    # Unseen categories in val/test map to 0.0
                    cat_df[f"{col}_freq"] = filled_series.map(freq_map).fillna(0.0)
                elif col in self.onehot_categories_:
                    known_cats = self.onehot_categories_[col]
                    for cat in known_cats:
                        cat_df[f"{col}_{cat}"] = (filled_series == cat).astype(float)
            else:
                if col in self.freq_encodings_:
                    cat_df[f"{col}_freq"] = 0.0
                elif col in self.onehot_categories_:
                    for cat in self.onehot_categories_[col]:
                        cat_df[f"{col}_{cat}"] = 0.0

        transformed_parts.append(cat_df)

        # Concatenate transformed features
        X_out = pd.concat(transformed_parts, axis=1)

        # Align columns with feature_names_out_
        for col in self.feature_names_out_:
            if col not in X_out.columns:
                X_out[col] = 0.0

        X_out = X_out[self.feature_names_out_].copy()
        return X_out

    def fit_transform(self, X: pd.DataFrame, y: Optional[pd.Series] = None) -> pd.DataFrame:
        """Fit on X and transform X."""
        return self.fit(X, y).transform(X)

    def get_feature_names_out(self, input_features: Optional[List[str]] = None) -> List[str]:
        """Return list of transformed feature names."""
        return self.feature_names_out_
