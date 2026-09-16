"""Tests for citation extraction and validation — Phase 4."""
import pytest

from src.genai.citations import extract_citations, validate_citations


def test_extract_citations():
    """Verify inline citation extraction."""
    text = "Risk score [EVID-ML-001]. Feature contribution [SHAP-001]. Policy [RAG-001]."
    citations = extract_citations(text)

    assert "EVID-ML-001" in citations
    assert "SHAP-001" in citations
    assert "RAG-001" in citations


def test_validate_citations_flags_invalid():
    """Verify validate_citations flags fabricated citations."""
    text = "Valid [EVID-ML-001] and fake [RAG-999]."
    valid_set = {"EVID-ML-001", "RAG-001"}

    is_valid, extracted, invalid = validate_citations(text, valid_set)

    assert not is_valid
    assert "RAG-999" in invalid
