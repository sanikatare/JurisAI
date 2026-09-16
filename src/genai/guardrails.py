"""Input & Output Guardrails Engine — Phase 4 Part 14.

Implements deterministic safety controls:
    - Input prompt injection detection and sanitization.
    - Output decision language filter (neutralizing autonomous "freeze/block/definitely fraud" phrases).
    - JSON schema validation.
"""
from __future__ import annotations

import re
from typing import Dict, Any, Tuple
from src.utils.logger import get_logger

logger = get_logger("genai_guardrails")

PROMPT_INJECTION_PATTERNS = [
    r"ignore (all )?previous instructions",
    r"reveal (the )?system prompt",
    r"system prompt",
    r"delete from",
    r"drop table",
    r"update transactions",
    r"hidden api key",
    r"invent evidence",
    r"bypass safety",
]

FORBIDDEN_DECISION_PHRASES = [
    (re.compile(r"\b(definitely|100%|guaranteed)\s+fraud\b", re.IGNORECASE), "elevated transaction risk"),
    (re.compile(r"\bfreeze\s+(this\s+)?(card|account|user)\b", re.IGNORECASE), "flag transaction for secondary analyst review"),
    (re.compile(r"\bblock\s+(this\s+)?(card|account|user)\b", re.IGNORECASE), "escalate to risk operations queue"),
    (re.compile(r"\bapprove\s+this\s+transaction\b", re.IGNORECASE), "clear transaction based on low risk score"),
    (re.compile(r"\breject\s+this\s+transaction\b", re.IGNORECASE), "recommend analyst review"),
]


def check_input_prompt_injection(user_input: str) -> Tuple[bool, str]:
    """Inspect user prompt for prompt injection and malicious keywords.

    Returns:
        (is_safe, refusal_reason) tuple.
    """
    cleaned = user_input.lower()
    for pattern in PROMPT_INJECTION_PATTERNS:
        if re.search(pattern, cleaned):
            logger.warning("Prompt Injection Guardrail Triggered! Pattern matched: '%s'", pattern)
            return False, f"Request rejected by security guardrail (matched pattern: '{pattern}')."
    return True, ""


def sanitize_output_decision_language(text: str) -> str:
    """Neutralize non-compliant autonomous decision/enforcement phrases in LLM output.

    Converts illegal enforcement terms into compliant decision support language.
    """
    sanitized = text
    for pattern, replacement in FORBIDDEN_DECISION_PHRASES:
        if pattern.search(sanitized):
            logger.warning("Output Guardrail Triggered! Neutralizing phrase matching '%s'", pattern.pattern)
            sanitized = pattern.sub(replacement, sanitized)
    return sanitized
