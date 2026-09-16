"""Tests for deterministic Evidence Bundle Collector — Phase 4."""
import pytest
import pandas as pd

from src.genai.evidence import EvidenceCollector
from src.genai.schemas import EvidenceBundle, EvidenceItem


def test_evidence_collector_assembles_bundle():
    """Verify EvidenceCollector produces structured bundle with citation IDs."""
    collector = EvidenceCollector(model_dir="models")

    df_row = pd.DataFrame([{
        "TransactionID": 2987015,
        "TransactionAmt": 207.24,
        "card1": 1001,
        "DeviceInfo": "SM-G935F Build/NRD90M",
        "P_emaildomain": "gmail.com",
        "graph_shared_device_prior_tx_count": 8,
        "anomaly_score": 0.8250,
    }])

    bundle = collector.collect_evidence(transaction_id=2987015, df_row=df_row)

    assert isinstance(bundle, EvidenceBundle)
    assert bundle.transaction_id == 2987015
    assert len(bundle.all_evidence_items) > 0

    citation_ids = [item.citation_id for item in bundle.all_evidence_items]
    assert "EVID-ML-001" in citation_ids
    assert "EVID-GRAPH-001" in citation_ids
