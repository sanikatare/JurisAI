"""Master Investigation Service — Phase 4 Core Orchestrator.

Orchestrates Evidence Collection, RAG Policy Retrieval, Fraud Investigator Agent,
Reporting Agent, and Data Analyst Agent into a unified service.
"""
from __future__ import annotations

import os
from typing import Dict, Any, List, Optional
import pandas as pd

from src.genai.evidence import EvidenceCollector
from src.genai.rag.hybrid_retriever import HybridRAGRetriever
from src.genai.agents.fraud_investigator import FraudInvestigatorAgent
from src.genai.agents.reporting_agent import ReportingAgent
from src.genai.agents.data_analyst import DataAnalystAgent
from src.genai.schemas import (
    EvidenceBundle,
    InvestigationResponse,
    InvestigationReport,
    DataAnalystResponse,
)
from src.ml.experiment_runner import generate_synthetic_ieee_cis_dataset
from src.utils.logger import get_logger

logger = get_logger("investigation_service")


class FinSightGenAIService:
    """Master service for Phase 4 Investigation & Decision Support."""

    def __init__(self, kb_dir: str = "knowledge_base", model_dir: str = "models"):
        self.evidence_collector = EvidenceCollector(model_dir=model_dir)
        self.rag_retriever = HybridRAGRetriever(kb_dir=kb_dir)
        self.investigator_agent = FraudInvestigatorAgent()
        self.reporting_agent = ReportingAgent()
        self.data_analyst_agent = DataAnalystAgent()

        # Cache synthetic transaction lookup dataset
        self.transaction_store: Dict[int, pd.DataFrame] = {}
        self._init_sample_data()

    def _init_sample_data(self):
        """Populate transaction store with sample transactions."""
        df_sample = generate_synthetic_ieee_cis_dataset(n_samples=50, random_seed=42)
        for _, row in df_sample.iterrows():
            tx_id = int(row["TransactionID"])
            self.transaction_store[tx_id] = pd.DataFrame([row])
        logger.info("FinSightGenAIService initialized with %d transaction records.", len(self.transaction_store))

    def get_transaction_row(self, transaction_id: int) -> pd.DataFrame:
        """Fetch transaction row or generate fallback."""
        if transaction_id in self.transaction_store:
            return self.transaction_store[transaction_id]

        # Generate single row fallback
        df_single = generate_synthetic_ieee_cis_dataset(n_samples=1, random_seed=transaction_id)
        df_single["TransactionID"] = transaction_id
        return df_single

    def assemble_evidence_bundle(self, transaction_id: int, query: Optional[str] = None) -> EvidenceBundle:
        """Assemble complete EvidenceBundle for a transaction.

        Args:
            transaction_id: Transaction ID.
            query: Optional query context for RAG retrieval.

        Returns:
            EvidenceBundle.
        """
        df_row = self.get_transaction_row(transaction_id)

        search_text = query or f"fraud device sharing transaction amount high risk SOP"
        retrieved_chunks = self.rag_retriever.retrieve(search_text, top_k=3)

        bundle = self.evidence_collector.collect_evidence(
            transaction_id=transaction_id,
            df_row=df_row,
            retrieved_policy_chunks=retrieved_chunks,
        )
        return bundle

    def investigate_case(self, transaction_id: int, query: Optional[str] = None) -> InvestigationResponse:
        """Run full investigation pipeline for a transaction.

        Args:
            transaction_id: Target Transaction ID.
            query: Optional analyst inquiry.

        Returns:
            InvestigationResponse.
        """
        bundle = self.assemble_evidence_bundle(transaction_id, query=query)
        response = self.investigator_agent.investigate(bundle, analyst_query=query)
        return response

    def generate_case_report(self, transaction_id: int) -> InvestigationReport:
        """Generate markdown investigation report for a transaction."""
        bundle = self.assemble_evidence_bundle(transaction_id)
        report = self.reporting_agent.generate_report(bundle)
        return report

    def ask_analyst_question(self, question: str) -> DataAnalystResponse:
        """Process read-only analytics question via Data Analyst Agent."""
        return self.data_analyst_agent.query(question)
