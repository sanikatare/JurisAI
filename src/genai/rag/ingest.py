"""RAG Document Ingestion & Metadata Loader — Phase 4 Part 8.

Loads markdown and text documents from the knowledge_base/ directory,
extracting document titles, IDs, categories, and file paths.
"""
from __future__ import annotations

import os
import glob
from typing import List, Dict, Any
from src.utils.logger import get_logger

logger = get_logger("rag_ingest")


def load_knowledge_base_documents(kb_dir: str = "rag/documents") -> List[Dict[str, Any]]:
    """Recursively load all markdown policy documents from rag/documents/ directory.

    Args:
        kb_dir: Root path to knowledge base directory.

    Returns:
        List of document dictionaries containing metadata and raw text.
    """
    if not os.path.exists(kb_dir):
        if os.path.exists("rag/documents"):
            kb_dir = "rag/documents"
        elif os.path.exists("knowledge_base"):
            kb_dir = "knowledge_base"
        else:
            logger.warning("Knowledge base directory %s does not exist.", kb_dir)
            return []

    doc_files = glob.glob(os.path.join(kb_dir, "**", "*.md"), recursive=True)
    documents = []

    for file_path in doc_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            rel_path = os.path.relpath(file_path, kb_dir)
            category = os.path.dirname(rel_path) or "general"
            title = os.path.basename(file_path).replace(".md", "").replace("_", " ").title()

            # Extract Document ID if present
            doc_id = f"DOC-{os.path.basename(file_path).upper().replace('.MD', '')}"
            for line in content.split("\n"):
                if "Document ID" in line or "**Document ID**" in line:
                    parts = line.split(":")
                    if len(parts) > 1:
                        doc_id = parts[1].strip().replace("`", "").replace("*", "")

            documents.append({
                "document_id": doc_id,
                "title": title,
                "category": category,
                "file_path": file_path,
                "content": content,
            })
        except Exception as e:
            logger.error("Error reading knowledge base file %s: %s", file_path, e)

    logger.info("Loaded %d knowledge base documents from %s.", len(documents), kb_dir)
    return documents
