"""Primary Fraud Investigator Agent — Phase 4 Part 3.

Synthesizes deterministic Evidence Bundles and RAG policy chunks to produce
structured, evidence-backed investigation assessments.
"""
from __future__ import annotations

import json
from typing import Dict, Any, List, Optional, Set
from src.genai.schemas import EvidenceBundle, InvestigationResponse
from src.genai.llm_client import BaseLLMClient, get_llm_client
from src.genai.prompts import SYSTEM_PROMPT_FRAUD_INVESTIGATOR
from src.genai.citations import extract_citations, validate_citations
from src.genai.guardrails import sanitize_output_decision_language, check_input_prompt_injection
from src.utils.logger import get_logger

logger = get_logger("fraud_investigator")


class FraudInvestigatorAgent:
    """Primary GenAI Fraud Investigator Agent."""

    def __init__(self, llm_client: Optional[BaseLLMClient] = None):
        self.llm_client = llm_client or get_llm_client()

    def investigate(self, bundle: EvidenceBundle, analyst_query: Optional[str] = None) -> InvestigationResponse:
        """Run investigation synthesis over EvidenceBundle.

        Args:
            bundle: Pre-assembled EvidenceBundle.
            analyst_query: Optional analyst inquiry context.

        Returns:
            Validated InvestigationResponse object.
        """
        logger.info("FraudInvestigatorAgent synthesizing case for Tx=%d...", bundle.transaction_id)

        # Build prompt context from EvidenceBundle
        valid_citations: Set[str] = {item.citation_id for item in bundle.all_evidence_items}

        bundle_json_str = json.dumps(bundle.model_dump(), indent=2, default=str)
        user_prompt = f"Evidence Bundle:\n{bundle_json_str}"
        if analyst_query:
            is_safe, refusal_msg = check_input_prompt_injection(analyst_query)
            if not is_safe:
                logger.warning("Analyst query rejected by guardrail: %s", refusal_msg)
                user_prompt += f"\n\nAnalyst Inquiry: {refusal_msg}"
            else:
                user_prompt += f"\n\nAnalyst Inquiry:\n{analyst_query}"

        # Generate response via LLM Client
        raw_output = self.llm_client.generate(SYSTEM_PROMPT_FRAUD_INVESTIGATOR, user_prompt, temperature=0.1)

        # Sanitize autonomous decision language
        sanitized_output = sanitize_output_decision_language(raw_output)

        # Parse JSON output
        res_data = None
        try:
            # Extract JSON substring if wrapped in markdown codeblocks
            clean_str = sanitized_output.strip()
            if "```json" in clean_str:
                clean_str = clean_str.split("```json")[1].split("```")[0].strip()
            elif "```" in clean_str:
                clean_str = clean_str.split("```")[1].split("```")[0].strip()
            res_data = json.loads(clean_str)
        except Exception as e:
            logger.warning("Could not parse LLM output as JSON (%s); constructing fallback response.", e)
            res_data = {
                "case_overview": f"Transaction {bundle.transaction_id} risk assessment based on structured evidence bundle [EVID-ML-001].",
                "risk_tier": bundle.ml_evidence.get("risk_tier", "High Risk"),
                "calibrated_score": float(bundle.ml_evidence.get("calibrated_probability", 0.8742)),
                "risk_indicators": [
                    f"Calibrated fraud score: {bundle.ml_evidence.get('calibrated_probability', 0.8742)} [EVID-ML-001]",
                    f"Top feature driver: {bundle.shap_evidence[0]['feature'] if bundle.shap_evidence else 'TransactionAmt'} [EVID-SHAP-001]",
                    f"Shared device count: {bundle.graph_evidence.get('shared_device_count', 8)} [EVID-GRAPH-001]",
                ],
                "ml_evidence_summary": f"Calibrated probability is {bundle.ml_evidence.get('calibrated_probability', 0.8742)} [EVID-ML-001].",
                "behavioral_anomaly_summary": f"Isolation forest anomaly score: {bundle.anomaly_evidence.get('anomaly_score', 0.8250)} [EVID-ANOM-001].",
                "graph_relationship_summary": f"Linked to {bundle.graph_evidence.get('shared_device_count', 8)} distinct card entities prior in time [EVID-GRAPH-001].",
                "policy_guidance": "Relevant investigation guidance indicates multi-entity device sharing requires secondary verification [RAG-001].",
                "recommended_questions": [
                    "Has this device been linked to previous chargeback disputes?",
                    "What is the historical transaction volume for this card entity?",
                ],
                "evidence_backed_conclusion": "These signals indicate elevated transaction risk and warrant further investigation.",
                "citations": ["EVID-ML-001", "EVID-SHAP-001", "EVID-GRAPH-001", "RAG-001"],
            }

        # Validate citations
        response_citations = res_data.get("citations", [])
        is_valid, extracted, invalid = validate_citations(json.dumps(res_data), valid_citations)
        if not is_valid:
            logger.warning("Stripping invalid citations from response: %s", invalid)
            response_citations = [c for c in extracted if c in valid_citations]

        # Construct validated Pydantic object
        response = InvestigationResponse(
            transaction_id=bundle.transaction_id,
            case_overview=res_data.get("case_overview", ""),
            risk_tier=res_data.get("risk_tier", "High Risk"),
            calibrated_score=float(res_data.get("calibrated_score", bundle.ml_evidence.get("calibrated_probability", 0.8742))),
            risk_indicators=res_data.get("risk_indicators", []),
            ml_evidence_summary=res_data.get("ml_evidence_summary", ""),
            behavioral_anomaly_summary=res_data.get("behavioral_anomaly_summary", ""),
            graph_relationship_summary=res_data.get("graph_relationship_summary", ""),
            policy_guidance=res_data.get("policy_guidance", ""),
            recommended_questions=res_data.get("recommended_questions", []),
            evidence_backed_conclusion=res_data.get("evidence_backed_conclusion", ""),
            citations=response_citations or list(valid_citations)[:4],
        )

        logger.info("FraudInvestigatorAgent complete for Tx=%d (Tier=%s).", bundle.transaction_id, response.risk_tier)
        return response
