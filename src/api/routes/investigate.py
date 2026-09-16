"""Investigate API Route — Phase 4 Part 17.

POST /api/v1/investigate
"""
from __future__ import annotations

from typing import Dict, Any, Optional
from src.genai.services.investigation_service import FinSightGenAIService
from src.utils.logger import get_logger

logger = get_logger("api_investigate")
service = FinSightGenAIService()


def run_investigation(transaction_id: int, query: Optional[str] = None) -> Dict[str, Any]:
    """Execute full case investigation synthesis."""
    response = service.investigate_case(transaction_id, query=query)
    return {
        "status": "success",
        "investigation": response.model_dump(),
    }
