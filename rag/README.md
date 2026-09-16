# FinSight AI — RAG Knowledge Base & Artifact Store

## Overview
This directory manages policy documents, chunk artifacts, vector indexes, and retrieval evaluation benchmarks for FinSight AI's **Hybrid RAG Engine**.

---

## Directory Structure
```
rag/
├── documents/       # Raw Policy Knowledge Base SOPs (AML, Fraud, KYC, Risk Policy)
├── processed/       # Preprocessed document texts
├── chunks/          # Formatted chunk JSON artifacts
├── indexes/         # FAISS / NumPy Cosine similarity index files
├── metadata/        # Document metadata maps
├── evaluation/      # Retrieval precision/recall benchmark reports
└── README.md
```

## Runtime Code
The production implementation code resides in `src/genai/rag/` (`ingest.py`, `chunking.py`, `embeddings.py`, `vector_store.py`, `bm25_retriever.py`, `hybrid_retriever.py`).
