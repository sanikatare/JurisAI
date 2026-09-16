"""Hybrid Reciprocal Rank Fusion Retriever — Phase 4 Part 10.

Combines Dense Vector Retrieval (FAISS/Embeddings) and Lexical Search (BM25)
using Reciprocal Rank Fusion (RRF):
    RRF_score(chunk) = 1.0 / (60 + dense_rank) + 1.0 / (60 + bm25_rank)
"""
from __future__ import annotations

import os
from typing import List, Dict, Any, Tuple
from collections import defaultdict

from src.genai.rag.ingest import load_knowledge_base_documents
from src.genai.rag.chunking import chunk_document
from src.genai.rag.embeddings import EmbeddingGenerator
from src.genai.rag.vector_store import VectorStore
from src.genai.rag.bm25_retriever import BM25Retriever
from src.utils.logger import get_logger

logger = get_logger("rag_hybrid")


class HybridRAGRetriever:
    """Hybrid RAG search combining Dense vector similarity and BM25 lexical matching."""

    def __init__(self, kb_dir: str = "rag/documents"):
        self.kb_dir = kb_dir
        self.chunks: List[Dict[str, Any]] = []
        self.embedding_generator = EmbeddingGenerator()
        self.vector_store = VectorStore()
        self.bm25_retriever = BM25Retriever()
        self.is_indexed = False

        self.index_knowledge_base()

    def index_knowledge_base(self):
        """Load, chunk, embed, and index all documents in knowledge_base/."""
        docs = load_knowledge_base_documents(self.kb_dir)
        if not docs:
            logger.warning("No knowledge base documents found to index.")
            return

        all_chunks = []
        for doc in docs:
            doc_chunks = chunk_document(doc)
            all_chunks.extend(doc_chunks)

        if not all_chunks:
            logger.warning("Chunking produced 0 chunks.")
            return

        self.chunks = all_chunks
        texts = [c["text"] for c in all_chunks]

        # 1. Fit Dense Vector Store
        embeddings = self.embedding_generator.fit_transform(texts)
        self.vector_store.build_index(all_chunks, embeddings)

        # 2. Fit Lexical BM25 Retriever
        self.bm25_retriever.fit(all_chunks)

        self.is_indexed = True
        logger.info("HybridRAGRetriever successfully indexed %d chunks across %d documents.", len(all_chunks), len(docs))

    def retrieve(self, query: str, top_k: int = 5, rrf_k: int = 60) -> List[Dict[str, Any]]:
        """Retrieve top-k relevant policy chunks using Reciprocal Rank Fusion.

        Args:
            query: Natural language policy or risk question.
            top_k: Number of final chunks to return.
            rrf_k: RRF constant penalty (default 60).

        Returns:
            List of top-k chunk dictionaries with assigned citation IDs.
        """
        if not self.is_indexed or not self.chunks:
            logger.warning("Hybrid retriever is empty or unindexed.")
            return []

        # 1. Dense Retrieval
        query_vec = self.embedding_generator.transform_query(query)
        dense_results = self.vector_store.search(query_vec, top_k=top_k * 2)

        # 2. Lexical BM25 Retrieval
        bm25_results = self.bm25_retriever.search(query, top_k=top_k * 2)

        # 3. Reciprocal Rank Fusion
        rrf_scores: Dict[str, float] = defaultdict(float)
        chunk_map: Dict[str, Dict[str, Any]] = {}

        for rank, (chunk, _) in enumerate(dense_results):
            cid = chunk["chunk_id"]
            rrf_scores[cid] += 1.0 / (rrf_k + rank + 1)
            chunk_map[cid] = chunk

        for rank, (chunk, _) in enumerate(bm25_results):
            cid = chunk["chunk_id"]
            rrf_scores[cid] += 1.0 / (rrf_k + rank + 1)
            chunk_map[cid] = chunk

        sorted_cids = sorted(rrf_scores.keys(), key=lambda cid: rrf_scores[cid], reverse=True)[:top_k]

        fused_chunks = []
        for idx, cid in enumerate(sorted_cids):
            chunk = chunk_map[cid].copy()
            chunk["citation_id"] = f"RAG-{idx+1:03d}"
            chunk["rrf_score"] = round(rrf_scores[cid], 5)
            fused_chunks.append(chunk)

        logger.info("Hybrid RAG retrieved %d policy chunks for query: '%s'", len(fused_chunks), query)
        return fused_chunks
