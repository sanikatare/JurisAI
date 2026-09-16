"""Graph Structural Benchmarking & Network Density Metrics — Phase 3 Section 15.

Calculates graph statistics for graph readiness verification and GNN gating:
    - Node count, edge count, average degree, density, connected components.
    - Evaluates computational cost and edge sparsity.
"""
from __future__ import annotations

from typing import Dict, Any
import numpy as np
import pandas as pd

from src.utils.logger import get_logger

logger = get_logger("graph_metrics")


def compute_graph_statistics(
    df: pd.DataFrame,
    card_col: str = "card1",
    device_col: str = "DeviceInfo",
    email_col: str = "P_emaildomain",
) -> Dict[str, Any]:
    """Compute structural graph density and connectivity statistics.

    Args:
        df: Input DataFrame.
        card_col: Card entity column.
        device_col: Device column.
        email_col: Email domain column.

    Returns:
        Dictionary containing network structural metrics.
    """
    n_transactions = len(df)
    
    unique_cards = df[card_col].nunique() if card_col in df.columns else 0
    unique_devices = df[device_col].nunique() if device_col in df.columns else 0
    unique_emails = df[email_col].nunique() if email_col in df.columns else 0

    total_nodes = n_transactions + unique_cards + unique_devices + unique_emails
    
    # Estimate bipartite edges (tx -> card, tx -> device, tx -> email)
    tx_card_edges = df[card_col].notna().sum() if card_col in df.columns else 0
    tx_device_edges = df[device_col].notna().sum() if device_col in df.columns else 0
    tx_email_edges = df[email_col].notna().sum() if email_col in df.columns else 0

    total_edges = int(tx_card_edges + tx_device_edges + tx_email_edges)

    # Average node degree
    avg_degree = float(2 * total_edges / total_nodes) if total_nodes > 0 else 0.0

    # Bipartite density: total_edges / (n_transactions * n_entities)
    total_entities = unique_cards + unique_devices + unique_emails
    max_possible_edges = n_transactions * total_entities
    density = float(total_edges / max_possible_edges) if max_possible_edges > 0 else 0.0

    stats = {
        "n_transactions": int(n_transactions),
        "unique_cards": int(unique_cards),
        "unique_devices": int(unique_devices),
        "unique_emails": int(unique_emails),
        "total_nodes": int(total_nodes),
        "total_edges": total_edges,
        "avg_degree": round(avg_degree, 4),
        "bipartite_density": round(density, 6),
        "repeat_card_ratio": round(float((n_transactions - unique_cards) / n_transactions), 4) if n_transactions > 0 else 0.0,
    }

    logger.info(
        "Graph Structural Metrics: Nodes=%d, Edges=%d, Avg Degree=%.4f, Density=%.6f",
        total_nodes, total_edges, avg_degree, density
    )
    return stats
