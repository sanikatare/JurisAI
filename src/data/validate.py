"""Validation stage — Phase 2 Part 2 (Data Quality Audit).

Runs structural checks BEFORE any cleaning happens, and raises/logs
findings rather than silently fixing them. Cleaning decisions are made
explicitly in clean.py, informed by these findings — never automatically.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd

from src.utils.logger import get_logger

logger = get_logger("validate")


@dataclass
class ValidationReport:
    n_rows: int
    n_columns: int
    duplicate_rows: int
    duplicate_ids: int
    negative_amounts: int
    zero_amounts: int
    completely_empty_columns: list[str] = field(default_factory=list)
    constant_columns: list[str] = field(default_factory=list)
    invalid_time_rows: int = 0
    warnings: list[str] = field(default_factory=list)

    def as_dict(self) -> dict:
        return self.__dict__


def validate(df: pd.DataFrame, config: dict) -> ValidationReport:
    id_col = config["dataset"]["id_column"]
    time_col = config["dataset"]["time_column"]
    amount_col = config["dataset"]["amount_column"]

    report = ValidationReport(
        n_rows=len(df),
        n_columns=len(df.columns),
        duplicate_rows=int(df.duplicated().sum()),
        duplicate_ids=int(df[id_col].duplicated().sum()) if id_col in df.columns else -1,
        negative_amounts=int((df[amount_col] < 0).sum()) if amount_col in df.columns else -1,
        zero_amounts=int((df[amount_col] == 0).sum()) if amount_col in df.columns else -1,
    )

    report.completely_empty_columns = [c for c in df.columns if df[c].isna().all()]
    report.constant_columns = [c for c in df.columns if df[c].nunique(dropna=True) <= 1]

    if time_col in df.columns:
        # TransactionDT is documented as a monotonically-usable relative time
        # offset (seconds), not a calendar date — it should never be negative.
        report.invalid_time_rows = int((df[time_col] < 0).sum())

    if report.duplicate_ids > 0:
        report.warnings.append(
            f"{report.duplicate_ids} duplicate {id_col} values found — "
            "this would break a one_to_one primary key assumption downstream."
        )
    if report.negative_amounts > 0:
        report.warnings.append(
            f"{report.negative_amounts} rows have a negative {amount_col}. "
            "Financial transactions are not expected to be negative in this "
            "dataset's documented schema — flag for manual review, do NOT "
            "silently drop or clip without inspecting a sample first."
        )
    if report.zero_amounts > 0:
        report.warnings.append(
            f"{report.zero_amounts} rows have a zero {amount_col}. "
            "A $0 transaction is not necessarily invalid (e.g. an auth-only "
            "or declined attempt) — treat as a candidate signal, not an error, "
            "unless investigation shows otherwise."
        )
    if report.completely_empty_columns:
        report.warnings.append(
            f"{len(report.completely_empty_columns)} column(s) are 100% missing: "
            f"{report.completely_empty_columns[:10]}{'...' if len(report.completely_empty_columns) > 10 else ''}"
        )
    if report.constant_columns:
        report.warnings.append(
            f"{len(report.constant_columns)} column(s) are constant (<=1 unique value) "
            "and carry no predictive information: "
            f"{report.constant_columns[:10]}{'...' if len(report.constant_columns) > 10 else ''}"
        )

    for w in report.warnings:
        logger.warning(w)

    return report
