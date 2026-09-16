"""Configurable LLM Client Abstraction — Phase 4 Part 1.

Provides a unified interface for LLM completions:
    - Supports OpenAI, Google Gemini, and a deterministic Mock/Offline Fallback Provider.
    - Low temperature for analytical responses.
    - Fails gracefully if external APIs are unreachable or unconfigured.
"""
from __future__ import annotations

import os
import json
from typing import Dict, Any, Optional
from dotenv import load_dotenv

from src.utils.logger import get_logger

load_dotenv()
logger = get_logger("llm_client")


class BaseLLMClient:
    """Base interface for LLM clients."""

    def generate(self, system_prompt: str, user_prompt: str, temperature: float = 0.1) -> str:
        raise NotImplementedError


class MockLLMClient(BaseLLMClient):
    """Deterministic Mock/Offline LLM Provider for offline execution & testing."""

    def generate(self, system_prompt: str, user_prompt: str, temperature: float = 0.1) -> str:
        logger.info("Executing MockLLMClient (Offline Fallback Mode)...")
        
        # Check if the prompt requests structured JSON or specific sections
        if "InvestigationReport" in system_prompt or "Report" in system_prompt:
            return """# Financial Risk Investigation Report

## 1. Case Summary
Transaction 2987015 presents elevated risk indicators [EVID-ML-001].

## 2. ML & Explainability Evidence
The candidate model assigned a calibrated fraud probability of 0.8742 [EVID-ML-001].
Top contributing features [EVID-SHAP-001]:
- `TransactionAmt` (+0.3120 increased risk)
- `card1_prior_tx_count` (+0.1420 increased risk)

## 3. Graph & Anomaly Signals
The transaction device was shared across 8 distinct card entities prior to transaction time [EVID-GRAPH-001]. Anomaly score: 0.8250.

## 4. Policy Guidance
Relevant investigation guidance indicates that multi-entity device sharing requires secondary verification [RAG-001].

## 5. Investigation Conclusion
These signals indicate elevated transaction risk and warrant further analyst review.
"""

        elif "DataAnalyst" in system_prompt:
            return json.dumps({
                "question": "How many high-risk transactions occurred?",
                "generated_sql": "SELECT COUNT(*) FROM view_model_predictions_summary WHERE risk_tier = 'High Risk';",
                "explanation": "Calculates the total count of transactions categorized in the High Risk tier.",
            })

        else:
            return json.dumps({
                "case_overview": "Transaction 2987015 exhibits elevated risk characteristics based on model predictions and device-sharing patterns [EVID-ML-001].",
                "risk_tier": "High Risk",
                "calibrated_score": 0.8742,
                "risk_indicators": [
                    "High transaction amount relative to entity baseline [EVID-SHAP-001]",
                    "Device shared across 8 distinct card entities prior to transaction [EVID-GRAPH-001]",
                    "High isolation forest anomaly score (0.8250)",
                ],
                "ml_evidence_summary": "Calibrated ML probability of 0.8742 [EVID-ML-001]. Top feature driver: TransactionAmt [EVID-SHAP-001].",
                "behavioral_anomaly_summary": "Isolation forest assigned an anomaly score of 0.8250, indicating out-of-distribution behavior.",
                "graph_relationship_summary": "Device node linked to 8 distinct card nodes prior in time [EVID-GRAPH-001].",
                "policy_guidance": "According to POL-AML-2026-v1, device sharing across 3+ entities warrants secondary review [RAG-001].",
                "recommended_questions": [
                    "Has this device been associated with previous chargebacks?",
                    "What is the historical transaction volume for this card entity?",
                ],
                "evidence_backed_conclusion": "These signals indicate elevated transaction risk and warrant further investigation.",
                "citations": ["EVID-ML-001", "EVID-SHAP-001", "EVID-GRAPH-001", "RAG-001"],
            })


class OpenAILLMClient(BaseLLMClient):
    """OpenAI API Provider Client."""

    def __init__(self, api_key: str, model_name: str = "gpt-4o-mini"):
        import openai
        self.client = openai.OpenAI(api_key=api_key)
        self.model_name = model_name

    def generate(self, system_prompt: str, user_prompt: str, temperature: float = 0.1) -> str:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
            max_tokens=1500,
        )
        return response.choices[0].message.content or ""


class GeminiLLMClient(BaseLLMClient):
    """Google Gemini API Provider Client."""

    def __init__(self, api_key: str, model_name: str = "gemini-1.5-flash"):
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    def generate(self, system_prompt: str, user_prompt: str, temperature: float = 0.1) -> str:
        prompt = f"{system_prompt}\n\nUser Question:\n{user_prompt}"
        response = self.model.generate_content(
            prompt,
            generation_config={"temperature": temperature, "max_output_tokens": 1500}
        )
        return response.text or ""


def get_llm_client() -> BaseLLMClient:
    """Factory function returning configured LLM Client with automatic fallback."""
    provider = os.getenv("LLM_PROVIDER", "mock").lower()
    openai_key = os.getenv("OPENAI_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")

    if provider == "openai" and openai_key:
        try:
            model = os.getenv("LLM_MODEL", "gpt-4o-mini")
            logger.info("Initializing OpenAI LLM Client (model=%s)...", model)
            return OpenAILLMClient(api_key=openai_key, model_name=model)
        except Exception as e:
            logger.warning("Failed to initialize OpenAI client (%s); falling back to MockLLMClient.", e)

    elif provider == "gemini" and gemini_key:
        try:
            model = os.getenv("LLM_MODEL", "gemini-1.5-flash")
            logger.info("Initializing Gemini LLM Client (model=%s)...", model)
            return GeminiLLMClient(api_key=gemini_key, model_name=model)
        except Exception as e:
            logger.warning("Failed to initialize Gemini client (%s); falling back to MockLLMClient.", e)

    logger.info("Using MockLLMClient (Offline / Fallback Mode).")
    return MockLLMClient()
