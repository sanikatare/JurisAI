"""Cleaning stage — Phase 2 Part 4 (Data Cleaning Strategy).

Principles enforced here:
    - Never blindly delete rows.
    - Never blindly fill every missing value with zero.
    - Every transformation is logged to a transformation log (returned
      alongside the cleaned frame) so cleaning is auditable and reversible.
    - Decisions are driven by MEASURED properties (from validate.py /
      profile.py), not assumptions about which columns "should" be dropped.

This module does NOT do feature engineering — that is transform.py.
Cleaning only: drop truly uninformative columns, handle missingness
transparently, standardize dtypes/formatting, and never touch the target.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd

from src.utils.logger import get_logger

logger = get_logger("clean")


@dataclass
class TransformationLog:
    steps: list[dict] = field(default_factory=list)

    def record(self, action: str, detail: str) -> None:
        self.steps.append({"action": action, "detail": detail})
        logger.info("%s: %s", action, detail)


def clean(df: pd.DataFrame, config: dict, target_col: str) -> tuple[pd.DataFrame, TransformationLog]:
    log = TransformationLog()
    df = df.copy()

    # Protected columns are NEVER dropped by any automated step below,
    # regardless of missingness/constancy — the target, id, time, and
    # amount columns are structurally required by every downstream stage.
    protected = {target_col, config["dataset"]["id_column"],
                 config["dataset"]["time_column"], config["dataset"]["amount_column"]}
    threshold = config["cleaning"]["missing_threshold_drop"]

    # 1. Drop fully-empty and constant columns — measured, not assumed.
    fully_empty = [c for c in df.columns if c not in protected and df[c].isna().all()]
    constant = [c for c in df.columns
                if c not in protected and c not in fully_empty and df[c].nunique(dropna=True) <= 1]
    to_drop = fully_empty + constant
    if to_drop:
        df = df.drop(columns=to_drop)
        log.record("drop_uninformative_columns",
                    f"Dropped {len(to_drop)} columns that are 100% missing or constant: {to_drop}")

    # 2. Drop columns above the measured missing-value threshold from config,
    #    EXCEPT the target and id/time/amount columns, which are never dropped.
    high_missing = [
        c for c in df.columns
        if c not in protected and df[c].isna().mean() > threshold
    ]
    if high_missing:
        df = df.drop(columns=high_missing)
        log.record("drop_high_missing_columns",
                    f"Dropped {len(high_missing)} columns with >{threshold:.0%} missing "
                    f"(measured, not assumed): {high_missing}")

    # 3. Duplicate rows: flag, do not silently drop, since a duplicate
    #    TransactionID pair could indicate a real data issue worth
    #    investigating rather than an artifact to erase.
    dup_count = int(df.duplicated().sum())
    if dup_count > 0:
        log.record("flag_duplicate_rows",
                    f"{dup_count} fully duplicate rows detected and RETAINED. "
                    "Manual review recommended before Phase 3 — do not assume "
                    "these are safe to drop without checking whether they "
                    "represent legitimate repeated transactions.")

    # 4. Missingness handling — explicit, per-dtype, never a blanket fillna(0).
    #    We add an explicit "<col>_was_missing" indicator for numeric columns
    #    with partial missingness so the ML stage (Phase 3) can decide how to
    #    use it, rather than losing the missingness signal by silently imputing.
    numeric_cols = df.select_dtypes(include="number").columns
    for col in numeric_cols:
        if col in protected:
            continue
        missing_frac = df[col].isna().mean()
        if 0 < missing_frac <= threshold:
            indicator_col = f"{col}_was_missing"
            df[indicator_col] = df[col].isna().astype("int8")
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)
            log.record("impute_numeric_with_missingness_flag",
                        f"{col}: {missing_frac:.2%} missing -> filled with median "
                        f"({median_val}), added {indicator_col} to preserve the signal.")

    categorical_cols = df.select_dtypes(include="object").columns
    for col in categorical_cols:
        if col in protected:
            continue
        missing_frac = df[col].isna().mean()
        if 0 < missing_frac <= threshold:
            df[col] = df[col].fillna("missing")
            log.record("impute_categorical_as_explicit_category",
                        f"{col}: {missing_frac:.2%} missing -> filled with explicit "
                        "'missing' category (not a mode/blind-zero fill, so the "
                        "model can learn from missingness itself).")

    # 5. Standardize categorical formatting (trim whitespace, consistent case)
    #    without changing the SET of categories present in the actual data.
    for col in categorical_cols:
        if df[col].dtype == object:
            df[col] = df[col].astype(str).str.strip()
    log.record("standardize_categorical_formatting", "Trimmed whitespace on all object columns.")

    return df, log
