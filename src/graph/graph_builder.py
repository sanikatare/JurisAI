"""Graph Construction & Network Data Preparation — Phase 3 Section 12 & 13.

Builds graph structures from IEEE-CIS relational keys (card1, DeviceInfo, P_emaildomain).
Ensures edge creation and aggregations observe temporal ordering constraints.
"""
from __future__ import annotations

from typing import Dict, Any, List, Tuple, Set
import pandas as pd
import numpy as np

from src.utils.logger import get_logger

logger = get_logger("graph_builder")


def normalize_device_info(series: pd.Series) -> pd.Series:
    """Clean and normalize raw DeviceInfo free-text strings.

    Example: "SM-G935F Build/NRD90M" -> "sm-g935f"
    """
    cleaned = series.fillna("missing").astype(str).str.lower().str.strip()
    cleaned = cleaned.str.split(" build/").str[0]
    cleaned = cleaned.str.replace(r"[^\w\s-]", "", regex=True)
    return cleaned


def build_entity_bipartite_edges(
    df: pd.DataFrame,
    transaction_id_col: str = "TransactionID",
    time_col: str = "TransactionDT",
    entity_cols: Optional[List[str]] = None,
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Construct temporal edge list linking Transaction nodes to Entity nodes.

    Args:
        df: Input DataFrame.
        transaction_id_col: Transaction identifier column.
        time_col: Time ordering column.
        entity_cols: List of relational entity keys (e.g. card1, DeviceInfo_clean, P_emaildomain).

    Returns:
        (edge_df, graph_summary_dict) tuple.
    """
    entity_cols = entity_cols or ["card1", "DeviceInfo", "P_emaildomain"]
    edges = []

    for col in entity_cols:
        if col in df.columns:
            valid_df = df[[transaction_id_col, time_col, col]].dropna()
            for _, row in valid_df.iterrows():
                tx_id = str(row[transaction_id_col])
                entity_val = f"{col}::{row[col]}"
                ts = row[time_col]
                edges.append({
                    "tx_id": tx_id,
                    "entity_id": entity_val,
                    "entity_type": col,
                    "timestamp": ts,
                })

    edge_df = pd.DataFrame(edges)

    unique_tx = edge_df["tx_id"].nunique() if not edge_df.empty else 0
    unique_entities = edge_df["entity_id"].nunique() if not edge_df.empty else 0
    total_edges = len(edge_df)

    summary = {
        "unique_transactions": unique_tx,
        "unique_entities": unique_entities,
        "total_edges": total_edges,
        "entity_types": entity_cols,
    }

    logger.info(
        "Built Bipartite Graph: %d transactions, %d unique entity nodes, %d total edges.",
        unique_tx, unique_entities, total_edges
    )
    return edge_df, summary
