"""Section-Aware Document Chunker — Phase 4 Part 9.

Splits documents into 300-500 token chunks preserving section headings and metadata context.
"""
from __future__ import annotations

import re
from typing import List, Dict, Any
from src.utils.logger import get_logger

logger = get_logger("rag_chunking")


def chunk_document(
    doc: Dict[str, Any],
    chunk_size_words: int = 150,  # ~300-400 tokens
    overlap_words: int = 30,
) -> List[Dict[str, Any]]:
    """Split a document into section-aware chunks with metadata context.

    Args:
        doc: Document dictionary from load_knowledge_base_documents.
        chunk_size_words: Target chunk size in words.
        overlap_words: Overlap size in words.

    Returns:
        List of chunk dictionaries with metadata.
    """
    content = doc["content"]
    doc_id = doc["document_id"]
    title = doc["title"]
    category = doc["category"]

    # Split by markdown headers ## or #
    sections = re.split(r"\n(?=#{1,3}\s)", content)
    chunks = []
    global_chunk_idx = 0

    for sec in sections:
        sec = sec.strip()
        if not sec:
            continue

        # Extract section heading if available
        heading = "General"
        lines = sec.split("\n")
        if lines[0].startswith("#"):
            heading = lines[0].lstrip("#").strip()

        words = sec.split()
        if len(words) <= chunk_size_words:
            global_chunk_idx += 1
            chunk_id = f"{doc_id}-CHK-{global_chunk_idx:03d}"
            chunks.append({
                "chunk_id": chunk_id,
                "document_id": doc_id,
                "title": title,
                "category": category,
                "heading": heading,
                "text": sec,
                "word_count": len(words),
            })
        else:
            # Sliding window over large sections
            start = 0
            while start < len(words):
                end = min(start + chunk_size_words, len(words))
                chunk_words = words[start:end]
                chunk_text = " ".join(chunk_words)

                # Include section heading context if missing
                if not chunk_text.startswith("#"):
                    chunk_text = f"## {heading} (Cont.)\n" + chunk_text

                global_chunk_idx += 1
                chunk_id = f"{doc_id}-CHK-{global_chunk_idx:03d}"
                chunks.append({
                    "chunk_id": chunk_id,
                    "document_id": doc_id,
                    "title": title,
                    "category": category,
                    "heading": heading,
                    "text": chunk_text,
                    "word_count": len(chunk_words),
                })
                start += (chunk_size_words - overlap_words)

    logger.info("Chunked document '%s' (%s) into %d chunks.", title, doc_id, len(chunks))
    return chunks
