"""Tests for leakage-safe graph feature engineering — Phase 3."""
import pytest
import pandas as pd
import numpy as np

from src.graph.graph_features import compute_leakage_safe_graph_features
from src.graph.graph_metrics import compute_graph_statistics
from src.graph.gnn_gate import evaluate_gnn_gate


def test_graph_features_never_look_forward_in_time():
    """Verify graph features use expanding prior windows."""
    df = pd.DataFrame({
        "TransactionID": [1, 2, 3],
        "TransactionDT": [100, 200, 300],
        "card1": [1001, 1001, 1001],
        "DeviceInfo": ["phone", "phone", "phone"],
        "P_emaildomain": ["gmail.com", "gmail.com", "gmail.com"],
        "TransactionAmt": [50.0, 100.0, 150.0],
    })

    df_graph = compute_leakage_safe_graph_features(df)

    # First transaction for card1 should have prior degree = 0
    assert df_graph["graph_card1_prior_degree"].iloc[0] == 0
    # Second transaction should have prior degree = 1
    assert df_graph["graph_card1_prior_degree"].iloc[1] == 1
    # Third transaction should have prior degree = 2
    assert df_graph["graph_card1_prior_degree"].iloc[2] == 2


def test_gnn_gate_decision_logic():
    """Verify GNN Gate returns NO-GO when performance improvement is insufficient."""
    stats = {"avg_degree": 1.2, "repeat_card_ratio": 0.02}
    res = evaluate_gnn_gate(graph_feature_pr_auc_delta=0.002, graph_stats=stats)

    assert res["decision"] == "NO-GO"
    assert "Graph feature engineering was evaluated" in res["justification"]
