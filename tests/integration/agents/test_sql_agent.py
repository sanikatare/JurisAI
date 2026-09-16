"""Tests for Read-Only Data Analyst SQL Agent — Phase 4."""
import pytest

from src.genai.agents.data_analyst import DataAnalystAgent, validate_sql_safety


def test_sql_safety_validator_rejects_dml_ddl():
    """Verify validate_sql_safety rejects non-SELECT or destructive SQL queries."""
    safe_sql = "SELECT COUNT(*) FROM view_model_predictions_summary WHERE risk_tier = 'High Risk';"
    is_safe, msg = validate_sql_safety(safe_sql)
    assert is_safe

    unsafe_sql_1 = "DELETE FROM fact_model_predictions WHERE transaction_id = 2987015;"
    is_safe_1, msg_1 = validate_sql_safety(unsafe_sql_1)
    assert not is_safe_1
    assert "Query must begin with SELECT" in msg_1 or "Forbidden SQL keyword" in msg_1

    unsafe_sql_2 = "SELECT * FROM view_model_predictions_summary; DROP TABLE fact_model_predictions;"
    is_safe_2, msg_2 = validate_sql_safety(unsafe_sql_2)
    assert not is_safe_2
    assert "Forbidden SQL keyword" in msg_2


def test_data_analyst_agent_query():
    """Verify DataAnalystAgent handles natural language analytics query."""
    agent = DataAnalystAgent()
    res = agent.query("How many high risk transactions occurred?")

    assert res.is_safe
    assert res.generated_sql.startswith("SELECT")
    assert len(res.query_results) > 0
