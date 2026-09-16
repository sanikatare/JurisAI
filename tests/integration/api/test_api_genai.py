"""Tests for REST API Endpoints & Master GenAI Service — Phase 4."""
import pytest

from src.genai.services.investigation_service import FinSightGenAIService
from src.api.routes import cases, investigate, ask, rag, report, analytics


def test_investigation_service_end_to_end():
    """Verify Master GenAI service orchestrates investigation flow."""
    service = FinSightGenAIService()

    # Investigate case
    res = service.investigate_case(2987015)
    assert res.transaction_id == 2987015
    assert res.risk_tier in ("High Risk", "Medium Risk", "Low Risk")

    # Report generation
    report = service.generate_case_report(2987015)
    assert report.transaction_id == 2987015
    assert len(report.markdown_content) > 100


def test_api_route_functions():
    """Verify route handler functions return structured outputs."""
    case_res = cases.get_case_details(2987015)
    assert case_res["status"] == "success"

    inv_res = investigate.run_investigation(2987015)
    assert inv_res["status"] == "success"

    ask_res = ask.ask_finsight("Why is this risky?", transaction_id=2987015)
    assert ask_res["status"] == "success"

    rag_res = rag.search_rag_knowledge_base("device sharing", top_k=2)
    assert rag_res["status"] == "success"

    rep_res = report.generate_report_endpoint(2987015)
    assert rep_res["status"] == "success"

    ana_res = analytics.run_analytics_query("Show fraud rate by product")
    assert ana_res["status"] == "success"
