"""SQL Analytics Agent API Route — Phase 4 Part 6.

POST /api/v1/analytics/query
"""
from __future__ import annotations

from typing import Dict, Any
from src.genai.services.investigation_service import FinSightGenAIService
from src.utils.logger import get_logger

logger = get_logger("api_analytics")
service = FinSightGenAIService()


def run_analytics_query(question: str) -> Dict[str, Any]:
    """Execute Data Analyst Agent SQL translation and safe query execution."""
    response = service.ask_analyst_question(question)
    return {
        "status": "success",
        "result": response.model_dump(),
    }
