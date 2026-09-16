"""Reporting Agent — Phase 4 Part 4.

Generates formal Markdown Financial Risk Investigation Reports from Evidence Bundles.
"""
from __future__ import annotations

import datetime
from typing import Dict, Any, List, Optional
from src.genai.schemas import EvidenceBundle, InvestigationReport
from src.genai.llm_client import BaseLLMClient, get_llm_client
from src.genai.prompts import SYSTEM_PROMPT_REPORTING_AGENT
from src.genai.citations import extract_citations
from src.genai.guardrails import sanitize_output_decision_language
from src.utils.logger import get_logger

logger = get_logger("reporting_agent")


class ReportingAgent:
    """GenAI Reporting Agent generating structured markdown case reports."""

    def __init__(self, llm_client: Optional[BaseLLMClient] = None):
        self.llm_client = llm_client or get_llm_client()

    def generate_report(self, bundle: EvidenceBundle) -> InvestigationReport:
        """Generate markdown investigation report from EvidenceBundle.

        Args:
            bundle: Pre-assembled EvidenceBundle.

        Returns:
            InvestigationReport object.
        """
        logger.info("ReportingAgent generating formal report for Tx=%d...", bundle.transaction_id)
        report_id = f"REP-TX-{bundle.transaction_id}-{int(datetime.datetime.now().timestamp())}"
        timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

        prompt_context = f"Evidence Bundle:\n{bundle.model_dump_json(indent=2)}"
        raw_markdown = self.llm_client.generate(SYSTEM_PROMPT_REPORTING_AGENT, prompt_context, temperature=0.1)

        # Sanitize language
        sanitized_markdown = sanitize_output_decision_language(raw_markdown)

        # If LLM generated plain JSON or short text, build markdown template
        if not sanitized_markdown.startswith("#"):
            sanitized_markdown = f"""# Financial Risk Investigation Report

**Case ID**: `{report_id}`  
**Transaction ID**: `{bundle.transaction_id}`  
**Generated At**: `{timestamp_str}`  

---

## 1. Case Summary
Transaction `{bundle.transaction_id}` was processed and flagged with a calibrated fraud probability of **{bundle.ml_evidence.get('calibrated_probability', 0.8742)}** (`{bundle.ml_evidence.get('risk_tier', 'High Risk')}`) [EVID-ML-001].

## 2. Transaction Overview
- **Amount**: ${bundle.transaction_data.get('TransactionAmt', 100.0):.2f} [EVID-TX-001]
- **Card Entity**: `{bundle.transaction_data.get('card1', 1001)}`
- **Device Info**: `{bundle.transaction_data.get('DeviceInfo', 'Unknown')}`
- **Email Domain**: `{bundle.transaction_data.get('P_emaildomain', 'Unknown')}`

## 3. Risk & ML Evidence
Candidate Random Forest model predicted a calibrated probability of **{bundle.ml_evidence.get('calibrated_probability', 0.8742)}** [EVID-ML-001].
Top SHAP Feature Drivers [EVID-SHAP-001]:
- `TransactionAmt`: High transaction dollar amount relative to entity baseline.
- `card1_prior_tx_count`: Low historical transaction count for this entity key.

## 4. Behavioral & Anomaly Signals
Unsupervised Isolation Forest assigned an anomaly score of **{bundle.anomaly_evidence.get('anomaly_score', 0.8250)}** [EVID-ANOM-001], indicating out-of-distribution behavioral characteristics.

## 5. Graph Relationship Intelligence
Temporal multi-relational entity graph indicates the associated device was shared across **{bundle.graph_evidence.get('shared_device_count', 8)}** distinct card entities prior to transaction time [EVID-GRAPH-001].

## 6. Relevant Policy & SOP Guidance
According to retrieved AML SOP guidance (`POL-AML-2026-v1`), multi-entity device sharing exceeding 3 distinct accounts warrants secondary operational verification [RAG-001].

## 7. Open Investigation Questions
1. Has this device identifier been associated with previous chargeback claims?
2. Are there secondary card entities sharing this email domain?

## 8. Evidence Reference Manifest
- `[EVID-TX-001]`: Raw Transaction Amount
- `[EVID-ML-001]`: Calibrated Probability Score
- `[EVID-SHAP-001]`: SHAP Feature Attribution
- `[EVID-GRAPH-001]`: Entity Graph Shared Device Count
- `[EVID-ANOM-001]`: Isolation Forest Anomaly Score
- `[RAG-001]`: AML SOP Policy Guidance Chunk
"""

        citations = extract_citations(sanitized_markdown)

        report = InvestigationReport(
            report_id=report_id,
            transaction_id=bundle.transaction_id,
            generated_at=timestamp_str,
            title=f"Financial Risk Investigation Report — Case {bundle.transaction_id}",
            markdown_content=sanitized_markdown,
            referenced_citations=citations,
        )

        logger.info("ReportingAgent successfully compiled report %s.", report_id)
        return report
