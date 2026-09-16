"""Tests for real-time Prediction Inference Service — Phase 5."""
import pytest
import pandas as pd

from src.services.prediction_service import PredictionService


def test_prediction_service_predict_transaction():
    """Verify PredictionService generates structured prediction response."""
    service = PredictionService()

    tx_data = {
        "TransactionID": 2987015,
        "TransactionDT": 86400,
        "TransactionAmt": 207.24,
        "card1": 1001,
        "DeviceInfo": "SM-G935F",
        "P_emaildomain": "gmail.com",
    }

    res = service.predict_transaction(tx_data)

    assert res["transaction_id"] == 2987015
    assert "calibrated_fraud_probability" in res
    assert res["risk_tier"] in ("High Risk", "Medium Risk", "Low Risk")
    assert "operating_threshold" in res
    assert "anomaly_score" in res
    assert "graph_risk_score" in res
