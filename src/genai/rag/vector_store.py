"""Dense Vector Store & Index — Phase 4 Part 10.

Maintains vector index over chunk embeddings using FAISS or Cosine Similarity fallback.
"""
from __future__ import annotations

from typing import List, Dict, Any, Tuple
import numpy as np

try:
    import faiss
    HAS_FAISS = True
except ImportError:
    HAS_FAISS = False

from src.utils.logger import get_logger

logger = get_logger("rag_vector_store")


class VectorStore:
    """In-memory or FAISS vector store for dense retrieval."""

    def __init__(self):
        self.chunks: List[Dict[str, Any]] = []
        self.embeddings: Optional[np.ndarray] = None
        self.faiss_index = None

    def build_index(self, chunks: List[Dict[str, Any]], embeddings: np.ndarray):
        """Build vector index from chunk metadata and embedding matrix."""
        self.chunks = chunks
        self.embeddings = embeddings.astype(np.float32)

        if HAS_FAISS:
            dim = embeddings.shape[1]
            self.faiss_index = faiss.IndexFlatIP(dim)  # Inner Product for normalized vectors = Cosine Similarity
            self.faiss_index.add(self.embeddings)
            logger.info("Built FAISS IndexFlatIP index with %d vectors (dim=%d).", len(chunks), dim)
        else:
            logger.info("FAISS not installed; built NumPy matrix Cosine Similarity vector store (%d chunks).", len(chunks))

    def search(self, query_vec: np.ndarray, top_k: int = 5) -> List[Tuple[Dict[str, Any], float]]:
        """Search top-k most similar chunks for query_vec.

        Returns:
            List of (chunk_dict, score) tuples.
        """
        if not self.chunks or self.embeddings is None:
            return []

        top_k = min(top_k, len(self.chunks))

        if HAS_FAISS and self.faiss_index is not None:
            scores, indices = self.faiss_index.search(query_vec, top_k)
            results = []
            for idx, score in zip(indices[0], scores[0]):
                if 0 <= idx < len(self.chunks):
                    results.append((self.chunks[idx], float(score)))
            return results
        else:
            # Cosine similarity via matrix multiplication
            scores = np.dot(self.embeddings, query_vec.T).squeeze()
            top_indices = np.argsort(scores)[::-1][:top_k]
            results = []
            for idx in top_indices:
                results.append((self.chunks[idx], float(scores[idx])))
            return results
