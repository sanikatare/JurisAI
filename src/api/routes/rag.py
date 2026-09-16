"""RAG Search API Route — Phase 4 Part 10.

POST /api/v1/rag/search
"""
from __future__ import annotations

from typing import Dict, Any
from src.genai.services.investigation_service import FinSightGenAIService
from src.utils.logger import get_logger

logger = get_logger("api_rag")
service = FinSightGenAIService()


def search_rag_knowledge_base(query: str, top_k: int = 5) -> Dict[str, Any]:
    """Execute hybrid dense + lexical RAG retrieval over policy documents."""
    chunks = service.rag_retriever.retrieve(query, top_k=top_k)
    return {
        "status": "success",
        "query": query,
        "count": len(chunks),
        "results": chunks,
    }
