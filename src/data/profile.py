"""Dataset profiling — Phase 2 Part 1 (Dataset Verification).

Computes, from the ACTUAL data (never assumed), for every column:
    data type, missing %, unique count, and a few validity signals.

This is deliberately schema-agnostic: it does not hardcode which IEEE-CIS
columns exist, because the brief explicitly forbids assuming/inventing
dataset structure. It profiles whatever it actually finds.

Run:
    python -m src.data.profile
Outputs:
    reports/data_profile.json          (machine-readable, full detail)
    reports/data_quality_report.md     (human-readable summary)
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from src.data.extract import extract_train, RawDataNotFoundError
from src.utils.config import load_config
from src.utils.logger import get_logger

logger = get_logger("profile")


def profile_dataframe(df: pd.DataFrame, target_col: str) -> dict:
    n_rows = len(df)
    profile = {"n_rows": n_rows, "n_columns": len(df.columns), "columns": {}}

    for col in df.columns:
        s = df[col]
        missing_pct = round(100 * s.isna().mean(), 4)
        unique_count = int(s.nunique(dropna=True))
        col_info = {
            "dtype": str(s.dtype),
            "missing_pct": missing_pct,
            "unique_count": unique_count,
            "is_constant": unique_count <= 1,
        }
        if pd.api.types.is_numeric_dtype(s):
            col_info.update({
                "min": float(s.min()) if n_rows else None,
                "max": float(s.max()) if n_rows else None,
                "mean": float(s.mean()) if n_rows else None,
                "n_negative": int((s < 0).sum()),
                "n_zero": int((s == 0).sum()),
            })
        profile["columns"][col] = col_info

    if target_col in df.columns:
        fraud_count = int(df[target_col].sum())
        profile["target"] = {
            "column": target_col,
            "fraud_count": fraud_count,
            "non_fraud_count": n_rows - fraud_count,
            "fraud_rate_pct": round(100 * fraud_count / n_rows, 4) if n_rows else None,
            "imbalance_ratio_nonfraud_to_fraud": round((n_rows - fraud_count) / fraud_count, 2)
            if fraud_count else None,
        }
    else:
        profile["target"] = {"column": target_col, "note": "target column not found in this frame"}

    profile["duplicate_row_count"] = int(df.duplicated().sum())
    id_col_candidates = [c for c in df.columns if c.lower().endswith("id")]
    profile["id_like_columns_duplicate_check"] = {
        c: int(df[c].duplicated().sum()) for c in id_col_candidates
    }

    return profile


def write_markdown_report(profile: dict, out_path: Path) -> None:
    lines = ["# Data Quality Report (auto-generated from actual data)\n"]
    lines.append(f"- Rows: {profile['n_rows']:,}")
    lines.append(f"- Columns: {profile['n_columns']}")
    lines.append(f"- Fully duplicate rows: {profile['duplicate_row_count']:,}\n")

    t = profile["target"]
    if "fraud_count" in t:
        lines.append("## Target quality\n")
        lines.append(f"- Fraud count: {t['fraud_count']:,}")
        lines.append(f"- Non-fraud count: {t['non_fraud_count']:,}")
        lines.append(f"- Fraud rate: {t['fraud_rate_pct']}%")
        lines.append(f"- Imbalance ratio (non-fraud : fraud): {t['imbalance_ratio_nonfraud_to_fraud']}:1\n")

    lines.append("## Column-level summary\n")
    lines.append("| Column | Dtype | Missing % | Unique Count | Constant? |")
    lines.append("|---|---|---|---|---|")
    for col, info in profile["columns"].items():
        lines.append(f"| {col} | {info['dtype']} | {info['missing_pct']} | "
                      f"{info['unique_count']} | {info['is_constant']} |")

    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    config = load_config()
    reports_dir = Path(config["paths"]["reports_dir"])
    reports_dir.mkdir(parents=True, exist_ok=True)

    try:
        df = extract_train(config)
    except RawDataNotFoundError as e:
        logger.error(str(e))
        print(str(e))
        return

    profile = profile_dataframe(df, config["dataset"]["target_column"])

    json_path = reports_dir / "data_profile.json"
    json_path.write_text(json.dumps(profile, indent=2), encoding="utf-8")
    logger.info("Wrote %s", json_path)

    md_path = reports_dir / "data_quality_report.md"
    write_markdown_report(profile, md_path)
    logger.info("Wrote %s", md_path)


if __name__ == "__main__":
    main()
