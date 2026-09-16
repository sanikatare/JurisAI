"""Embedding Vector Generator — Phase 4 Part 10.

Computes dense vector representations for text chunks:
    - Uses SentenceTransformers if installed (`all-MiniLM-L6-v2`).
    - Falls back to scikit-learn TF-IDF vectorization when SentenceTransformers is absent.
"""
from __future__ import annotations

from typing import List, Dict, Any
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from src.utils.logger import get_logger

logger = get_logger("rag_embeddings")


class EmbeddingGenerator:
    """Generates dense embedding vectors for RAG document chunks."""

    def __init__(self):
        self.st_model = None
        self.tfidf_vectorizer = None
        self.is_tfidf = True

        try:
            from sentence_transformers import SentenceTransformer
            self.st_model = SentenceTransformer("all-MiniLM-L6-v2")
            self.is_tfidf = False
            logger.info("SentenceTransformer embedding model loaded successfully.")
        except Exception:
            logger.info("SentenceTransformers not available; using TF-IDF dense vectorization fallback.")

    def fit_transform(self, texts: List[str]) -> np.ndarray:
        """Fit vectorizer on texts and return normalized embedding matrix."""
        if not self.is_tfidf and self.st_model is not None:
            embeddings = self.st_model.encode(texts, convert_to_numpy=True)
        else:
            self.tfidf_vectorizer = TfidfVectorizer(max_features=384, stop_words="english")
            embeddings = self.tfidf_vectorizer.fit_transform(texts).toarray()

        # L2 normalize
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        return (embeddings / norms).astype(np.float32)

    def transform_query(self, query: str) -> np.ndarray:
        """Transform a single search query string into embedding vector."""
        if not self.is_tfidf and self.st_model is not None:
            vec = self.st_model.encode([query], convert_to_numpy=True)
        else:
            if self.tfidf_vectorizer is None:
                raise ValueError("EmbeddingGenerator must be fit before transform_query.")
            vec = self.tfidf_vectorizer.transform([query]).toarray()

        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        return vec.astype(np.float32)
