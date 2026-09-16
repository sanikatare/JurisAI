"""Cases API Routes — Phase 4 Part 16.

GET /api/v1/cases/{transaction_id}
GET /api/v1/cases/{transaction_id}/evidence
"""
from __future__ import annotations

from typing import Dict, Any
from src.genai.services.investigation_service import FinSightGenAIService
from src.utils.logger import get_logger

logger = get_logger("api_cases")
service = FinSightGenAIService()


def get_case_details(transaction_id: int) -> Dict[str, Any]:
    """Retrieve case details and transaction summary."""
    df_row = service.get_transaction_row(transaction_id)
    return {
        "status": "success",
        "transaction_id": transaction_id,
        "transaction_data": df_row.iloc[0].to_dict(),
    }


def get_case_evidence(transaction_id: int) -> Dict[str, Any]:
    """Retrieve deterministic EvidenceBundle for a case."""
    bundle = service.assemble_evidence_bundle(transaction_id)
    return {
        "status": "success",
        "transaction_id": transaction_id,
        "evidence_bundle": bundle.model_dump(),
    }
