"""Tests for hybrid RAG pipeline — Phase 4."""
import pytest

from src.genai.rag.ingest import load_knowledge_base_documents
from src.genai.rag.chunking import chunk_document
from src.genai.rag.hybrid_retriever import HybridRAGRetriever


def test_knowledge_base_ingestion_and_chunking():
    """Verify markdown knowledge base ingestion and chunking."""
    docs = load_knowledge_base_documents(kb_dir="rag/documents")
    assert len(docs) > 0

    chunks = chunk_document(docs[0])
    assert len(chunks) > 0
    assert "text" in chunks[0]
    assert "chunk_id" in chunks[0]


def test_hybrid_rag_retrieval():
    """Verify hybrid retriever returns chunks with RAG citations."""
    retriever = HybridRAGRetriever(kb_dir="rag/documents")
    results = retriever.retrieve("device sharing velocity AML SOP", top_k=3)

    assert len(results) > 0
    assert "citation_id" in results[0]
    assert results[0]["citation_id"].startswith("RAG-")
