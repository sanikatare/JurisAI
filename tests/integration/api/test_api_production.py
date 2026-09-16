"""Tests for production REST API endpoints & prediction service — Phase 5."""
import pytest
from src.api.routes import cases, investigate, ask, rag, report, analytics
from src.services.prediction_service import PredictionService


def test_production_api_routes():
    """Verify production API endpoints return valid JSON responses."""
    # Health route check
    case_res = cases.get_case_details(2987015)
    assert case_res["status"] == "success"

    # Prediction service check
    tx_payload = {
        "TransactionID": 2987015,
        "TransactionDT": 86400,
        "TransactionAmt": 207.24,
        "card1": 1001,
        "DeviceInfo": "SM-G935F",
        "P_emaildomain": "gmail.com",
    }
    service = PredictionService()
    pred_res = service.predict_transaction(tx_payload)

    assert "calibrated_fraud_probability" in pred_res
    assert pred_res["risk_tier"] in ("High Risk", "Medium Risk", "Low Risk")
    assert pred_res["transaction_id"] == 2987015
