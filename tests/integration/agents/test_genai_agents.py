"""Tests for GenAI Agents (Fraud Investigator & Reporting) — Phase 4."""
import pytest
import pandas as pd

from src.genai.evidence import EvidenceCollector
from src.genai.agents.fraud_investigator import FraudInvestigatorAgent
from src.genai.agents.reporting_agent import ReportingAgent
from src.genai.schemas import InvestigationResponse, InvestigationReport


def test_fraud_investigator_agent():
    """Verify FraudInvestigatorAgent synthesizes structured evidence response."""
    collector = EvidenceCollector(model_dir="models")
    df_row = pd.DataFrame([{
        "TransactionID": 2987015,
        "TransactionAmt": 207.24,
        "card1": 1001,
        "DeviceInfo": "SM-G935F",
        "P_emaildomain": "gmail.com",
    }])
    bundle = collector.collect_evidence(2987015, df_row)

    agent = FraudInvestigatorAgent()
    response = agent.investigate(bundle)

    assert isinstance(response, InvestigationResponse)
    assert response.transaction_id == 2987015
    assert response.risk_tier in ("High Risk", "Medium Risk", "Low Risk")
    assert len(response.citations) > 0


def test_reporting_agent_generates_markdown():
    """Verify ReportingAgent produces valid markdown report."""
    collector = EvidenceCollector(model_dir="models")
    df_row = pd.DataFrame([{
        "TransactionID": 2987015,
        "TransactionAmt": 207.24,
        "card1": 1001,
    }])
    bundle = collector.collect_evidence(2987015, df_row)

    agent = ReportingAgent()
    report = agent.generate_report(bundle)

    assert isinstance(report, InvestigationReport)
    assert report.transaction_id == 2987015
    assert "# Financial Risk Investigation Report" in report.markdown_content
