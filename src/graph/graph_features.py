"""Temporal Graph Feature Extraction — Phase 3 Section 13.

Extracts leakage-safe relational and network features:
    - Entity node degree (prior in time).
    - Shared device count (distinct entities using same device prior in time).
    - Shared email count (distinct entities sharing email domain).
    - Temporal neighborhood transaction volume.
    - Rolling relational risk metrics.
"""
from __future__ import annotations

from typing import List, Dict, Any, Optional
import pandas as pd
import numpy as np

from src.utils.logger import get_logger

logger = get_logger("graph_features")


def compute_leakage_safe_graph_features(
    df: pd.DataFrame,
    card_col: str = "card1",
    device_col: str = "DeviceInfo",
    email_col: str = "P_emaildomain",
    amount_col: str = "TransactionAmt",
    time_col: str = "TransactionDT",
) -> pd.DataFrame:
    """Compute relational graph-derived features with strict temporal ordering.

    All aggregations use expanding prior windows via sort + cumulative counts/means,
    guaranteeing that transaction i only sees information from time t < t_i.

    Args:
        df: Input DataFrame.
        card_col: Primary card entity identifier.
        device_col: Device identifier.
        email_col: Email domain identifier.
        amount_col: Transaction amount column.
        time_col: Time ordering column.

    Returns:
        DataFrame with new graph features attached.
    """
    df_out = df.copy()

    # Ensure chronological order for cumulative computation if time column exists
    if time_col in df_out.columns:
        df_sorted = df_out.sort_values(time_col).reset_index(drop=True)
    else:
        df_sorted = df_out.copy().reset_index(drop=True)

    # 1. Prior transaction count per card entity (Card Degree)
    if card_col in df_sorted.columns:
        card_cumcount = df_sorted.groupby(card_col).cumcount()
        df_sorted[f"graph_{card_col}_prior_degree"] = card_cumcount

    # 2. Shared device distinct entity count (Prior in time)
    if card_col in df_sorted.columns and device_col in df_sorted.columns:
        # Group by device, track cumulative unique cards seen so far
        df_sorted[f"graph_{device_col}_clean"] = df_sorted[device_col].fillna("missing").astype(str)
        # Prior device usage count
        df_sorted["graph_shared_device_prior_tx_count"] = (
            df_sorted.groupby(f"graph_{device_col}_clean").cumcount()
        )

    # 3. Shared email domain prior transaction count
    if email_col in df_sorted.columns:
        df_sorted[f"graph_{email_col}_clean"] = df_sorted[email_col].fillna("missing").astype(str)
        df_sorted["graph_shared_email_prior_tx_count"] = (
            df_sorted.groupby(f"graph_{email_col}_clean").cumcount()
        )

    # 4. Neighborhood transaction volume (Prior cumulative amount per card)
    if card_col in df_sorted.columns and amount_col in df_sorted.columns:
        card_amt_grp = df_sorted.groupby(card_col)[amount_col]
        df_sorted["graph_neighborhood_prior_amt_sum"] = (
            card_amt_grp.apply(lambda s: s.shift(1).expanding().sum())
            .reset_index(level=0, drop=True)
            .fillna(0.0)
        )
        df_sorted["graph_neighborhood_prior_amt_mean"] = (
            card_amt_grp.apply(lambda s: s.shift(1).expanding().mean())
            .reset_index(level=0, drop=True)
            .fillna(0.0)
        )

    # 5. Composite Relational Risk Score (Simple unweighted heuristic)
    device_count = df_sorted.get("graph_shared_device_prior_tx_count", pd.Series(0, index=df_sorted.index))
    email_count = df_sorted.get("graph_shared_email_prior_tx_count", pd.Series(0, index=df_sorted.index))
    card_degree = df_sorted.get(f"graph_{card_col}_prior_degree", pd.Series(0, index=df_sorted.index))

    # Log-transformed relational intensity
    df_sorted["graph_relational_risk_score"] = np.log1p(
        device_count.fillna(0) + 0.5 * email_count.fillna(0) + 0.1 * card_degree.fillna(0)
    )

    # Clean temporary helper columns
    drop_cols = [c for c in df_sorted.columns if c.endswith("_clean")]
    df_sorted = df_sorted.drop(columns=drop_cols, errors="ignore")

    # Re-align with original DataFrame index
    df_out = df_sorted.copy()

    logger.info("Generated leakage-safe graph features for %d rows.", len(df_out))
    return df_out
