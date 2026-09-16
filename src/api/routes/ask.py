"""Ask FinSight Q&A API Route — Phase 4 Part 5.

POST /api/v1/ask
"""
from __future__ import annotations

from typing import Dict, Any, Optional
from src.genai.services.investigation_service import FinSightGenAIService
from src.genai.guardrails import check_input_prompt_injection
from src.utils.logger import get_logger

logger = get_logger("api_ask")
service = FinSightGenAIService()


def ask_finsight(question: str, transaction_id: Optional[int] = None) -> Dict[str, Any]:
    """Process natural language analyst query."""
    is_safe, refusal_reason = check_input_prompt_injection(question)
    if not is_safe:
        return {
            "status": "error",
            "error": refusal_reason,
        }

    tx_id = transaction_id or 2987015
    investigation = service.investigate_case(tx_id, query=question)
    return {
        "status": "success",
        "question": question,
        "answer": investigation.case_overview,
        "risk_summary": investigation.evidence_backed_conclusion,
        "citations": investigation.citations,
    }
