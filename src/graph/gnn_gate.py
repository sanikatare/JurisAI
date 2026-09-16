"""GNN Go/No-Go Decision Gate — Phase 3 Section 15.

Evaluates empirical graph performance deltas and structural metrics to determine whether
implementing a Deep Graph Neural Network (e.g. GraphSAGE) is justified over graph feature engineering.
"""
from __future__ import annotations

from typing import Dict, Any
from src.utils.logger import get_logger

logger = get_logger("gnn_gate")


def evaluate_gnn_gate(
    graph_feature_pr_auc_delta: float,
    graph_stats: Dict[str, Any],
    min_pr_auc_improvement: float = 0.01,
    min_avg_degree: float = 1.5,
    min_repeat_card_ratio: float = 0.05,
) -> Dict[str, Any]:
    """Execute GNN Go/No-Go Gate Decision Logic.

    Args:
        graph_feature_pr_auc_delta: PR-AUC delta gained by adding graph features.
        graph_stats: Output dictionary from compute_graph_statistics.
        min_pr_auc_improvement: Minimum PR-AUC improvement required.
        min_avg_degree: Minimum average degree required.
        min_repeat_card_ratio: Minimum repeat card transaction ratio.

    Returns:
        Dictionary containing decision ("GO" or "NO-GO"), justification, and detailed breakdown.
    """
    avg_degree = graph_stats.get("avg_degree", 0.0)
    repeat_card_ratio = graph_stats.get("repeat_card_ratio", 0.0)

    cond_performance = graph_feature_pr_auc_delta >= min_pr_auc_improvement
    cond_density = (avg_degree >= min_avg_degree) or (repeat_card_ratio >= min_repeat_card_ratio)

    go_decision = cond_performance and cond_density

    if go_decision:
        status = "GO"
        recommendation = "Proceed to GNN candidate evaluation (e.g., GraphSAGE) in Phase 4."
        justification = (
            f"Graph features provided meaningful PR-AUC improvement (+{graph_feature_pr_auc_delta:.4f} >= {min_pr_auc_improvement}) "
            f"and graph structural metrics confirm sufficient edge density (avg_degree={avg_degree:.2f}, repeat_card_ratio={repeat_card_ratio:.4f})."
        )
    else:
        status = "NO-GO"
        recommendation = "Maintain graph feature engineering as the primary relational approach; do NOT implement full GNN."
        justification = (
            f"Graph feature engineering was evaluated as the appropriate relational approach for the selected dataset; "
            f"a full GNN was not justified based on graph density/performance/complexity "
            f"(PR-AUC delta: {graph_feature_pr_auc_delta:+.4f} vs threshold {min_pr_auc_improvement}, "
            f"avg_degree: {avg_degree:.2f}, repeat_card_ratio: {repeat_card_ratio:.4f})."
        )

    decision_summary = {
        "decision": status,
        "recommendation": recommendation,
        "justification": justification,
        "metrics_evaluated": {
            "graph_feature_pr_auc_delta": round(graph_feature_pr_auc_delta, 5),
            "avg_degree": round(avg_degree, 4),
            "repeat_card_ratio": round(repeat_card_ratio, 4),
            "cond_performance_passed": cond_performance,
            "cond_density_passed": cond_density,
        },
    }

    logger.info("GNN Gate Decision: %s — %s", status, justification)
    return decision_summary
