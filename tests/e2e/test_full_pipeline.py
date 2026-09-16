"""End-to-End Pipeline Automated Smoke Test — Phase 6 Part A.

Verifies the complete 15-step financial risk intelligence workflow:
Transaction Payload -> Validation -> Preprocessing -> Model Prediction -> Anomaly Detection
 -> Graph Risk Features -> Calibration -> SHAP Explanation -> Evidence Bundle
 -> RAG Retrieval -> GenAI Investigation -> Response Validation.
"""
import pytest
import pandas as pd
import numpy as np

from src.data.validate import validate
from src.services.prediction_service import PredictionService
from src.genai.evidence import EvidenceCollector
from src.genai.rag.hybrid_retriever import HybridRAGRetriever
from src.genai.agents.fraud_investigator import FraudInvestigatorAgent
from src.genai.guardrails import check_input_prompt_injection, sanitize_output_decision_language
from src.api.routes.cases import get_case_details


def test_full_pipeline_e2e_smoke():
    """Execute complete end-to-end transaction validation to AI investigation flow."""
    # 1. Input Transaction Payload
    raw_payload = {
        "TransactionID": 2987015,
        "TransactionDT": 86400,
        "TransactionAmt": 207.24,
        "ProductCD": "W",
        "card1": 1001,
        "card2": 555.0,
        "card3": 150.0,
        "card4": "visa",
        "card5": 226.0,
        "card6": "debit",
        "P_emaildomain": "gmail.com",
        "R_emaildomain": "gmail.com",
        "DeviceInfo": "SM-G935F",
        "DeviceType": "desktop",
    }

    # 2. Schema Validation
    df_raw = pd.DataFrame([raw_payload])
    cfg = {
        "dataset": {
            "id_column": "TransactionID",
            "time_column": "TransactionDT",
            "amount_column": "TransactionAmt",
        }
    }
    val_report = validate(df_raw, cfg)
    assert val_report.n_rows == 1
    assert val_report.duplicate_rows == 0

    # 3. Prediction & Risk Scoring Pipeline (ML + Anomaly + Graph + Calibration + SHAP)
    service = PredictionService()
    pred_res = service.predict_transaction(raw_payload)

    assert pred_res["transaction_id"] == 2987015
    assert "calibrated_fraud_probability" in pred_res
    assert 0.0 <= pred_res["calibrated_fraud_probability"] <= 1.0
    assert pred_res["risk_tier"] in ("High Risk", "Medium Risk", "Low Risk")
    assert "operating_threshold" in pred_res
    assert "anomaly_score" in pred_res
    assert "graph_risk_score" in pred_res
    assert isinstance(pred_res["top_shap_features"], list)

    # 4. Evidence Bundle Creation
    collector = EvidenceCollector()
    bundle = collector.collect_evidence(2987015, df_raw)
    assert bundle.transaction_id == 2987015
    assert bundle.ml_evidence["risk_tier"] in ("High Risk", "Medium Risk", "Low Risk")

    # 5. Hybrid RAG Policy Retrieval
    retriever = HybridRAGRetriever()
    rag_docs = retriever.retrieve("What is the step-up verification requirement for high risk transactions?", top_k=2)
    assert isinstance(rag_docs, list)
    from src.genai.guardrails import check_input_prompt_injection, sanitize_output_decision_language

    # 6. Fraud Investigator Agent & Citation Guardrails
    is_safe, refusal = check_input_prompt_injection("Explain why transaction 2987015 was flagged.")
    assert is_safe is True

    investigator = FraudInvestigatorAgent()
    investigation = investigator.investigate(bundle, analyst_query="Explain why transaction 2987015 was flagged.")
    assert investigation.transaction_id == 2987015
    assert investigation.risk_tier in ("High Risk", "Medium Risk", "Low Risk")
    from src.api.routes.investigate import run_investigation

    # 7. End-to-End REST Service Route Integration
    service_res = run_investigation(2987015)
    assert service_res["status"] == "success"
    assert "investigation" in service_res
