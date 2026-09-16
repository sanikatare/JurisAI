"""Report Generation API Route — Phase 4 Part 4.

POST /api/v1/report
"""
from __future__ import annotations

from typing import Dict, Any
from src.genai.services.investigation_service import FinSightGenAIService
from src.utils.logger import get_logger

logger = get_logger("api_report")
service = FinSightGenAIService()


def generate_report_endpoint(transaction_id: int) -> Dict[str, Any]:
    """Generate Markdown Financial Risk Investigation Report."""
    report = service.generate_case_report(transaction_id)
    return {
        "status": "success",
        "report": report.model_dump(),
    }
