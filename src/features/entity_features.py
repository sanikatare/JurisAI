"""Entity/behavioral feature engineering — Phase 2 Part 10.

Only built for identifiers actually present and usable as entity keys in
the real data (per docs/graph_readiness_audit.md) — e.g. card1 as a proxy
account identifier, or a constructed device/email key. This module does
NOT assume a specific column exists; the caller passes the entity_col
name after confirming it via the graph readiness audit.

CRITICAL leakage rule: every rolling/expanding statistic for row i is
computed using `.shift(1)` (or an explicitly `closed="left"` window)
so it reflects only transactions STRICTLY BEFORE row i in time, never
including row i itself. Using a window that includes the current row
would leak the very amount/label the model is trying to predict.
"""
from __future__ import annotations

import pandas as pd

from src.utils.logger import get_logger

logger = get_logger("entity_features")


def add_entity_rolling_features(
    df: pd.DataFrame, entity_col: str, amount_col: str, time_col: str
) -> pd.DataFrame:
    """Add prior-transaction-count and prior-amount statistics per entity.

    All statistics use `.shift(1)` after an expanding window, meaning
    "computed from every transaction this entity made before this one,"
    which is exactly the leakage-safe framing Phase 1 requires.
    """
    df = df.copy()
    df = df.sort_values([entity_col, time_col])

    grp = df.groupby(entity_col)[amount_col]

    df[f"{entity_col}_prior_tx_count"] = grp.cumcount()  # count of PRIOR tx, 0 for the first
    df[f"{entity_col}_prior_amount_mean"] = grp.apply(
        lambda s: s.shift(1).expanding().mean()
    ).reset_index(level=0, drop=True)
    df[f"{entity_col}_prior_amount_max"] = grp.apply(
        lambda s: s.shift(1).expanding().max()
    ).reset_index(level=0, drop=True)
    df[f"{entity_col}_amount_deviation_from_prior_mean"] = (
        df[amount_col] - df[f"{entity_col}_prior_amount_mean"]
    )

    logger.info(
        "Added leakage-safe rolling features for entity_col=%s: prior_tx_count, "
        "prior_amount_mean, prior_amount_max, amount_deviation_from_prior_mean "
        "(all computed with shift(1), so row i never sees its own amount).",
        entity_col,
    )
    return df


def add_shared_identifier_flags(df: pd.DataFrame, identifier_cols: list[str]) -> pd.DataFrame:
    """Flag whether an identifier value (e.g. device, email domain) is shared
    across more than one distinct entity — a precursor graph-readiness signal
    (Phase 1 Part 14 / Phase 2 Part 12), computed WITHOUT building a full graph.

    NOTE: this uses global (not time-restricted) counts, so it is a
    descriptive/graph-readiness signal for EDA, not yet a leakage-safe model
    feature. If promoted to a Phase 3 model feature, it must be recomputed
    using only prior-in-time occurrences, same as the rolling stats above.
    """
    df = df.copy()
    for col in identifier_cols:
        if col not in df.columns:
            logger.warning("Identifier column %s not found — skipping.", col)
            continue
        counts = df[col].value_counts()
        df[f"{col}_global_share_count"] = df[col].map(counts)
        logger.info("Added %s_global_share_count (descriptive/EDA use only — "
                    "see docstring on leakage caveat before using in Phase 3 models).", col)
    return df
