"""Lexical BM25 Search Engine — Phase 4 Part 10.

Implements BM25 lexical keyword matching over chunk texts.
"""
from __future__ import annotations

import math
import re
from typing import List, Dict, Any, Tuple
from collections import Counter

from src.utils.logger import get_logger

logger = get_logger("rag_bm25")


class BM25Retriever:
    """Lightweight BM25 Okapi lexical retriever."""

    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.chunks: List[Dict[str, Any]] = []
        self.doc_len: List[int] = []
        self.avg_doc_len: float = 0.0
        self.doc_freqs: List[Counter] = []
        self.idf: Dict[str, float] = {}

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r"\w+", text.lower())

    def fit(self, chunks: List[Dict[str, Any]]):
        """Fit BM25 statistics on chunk texts."""
        self.chunks = chunks
        self.doc_freqs = []
        self.doc_len = []

        total_words = 0
        df_counter = Counter()

        for chunk in chunks:
            tokens = self._tokenize(chunk["text"])
            self.doc_len.append(len(tokens))
            total_words += len(tokens)
            freqs = Counter(tokens)
            self.doc_freqs.append(freqs)
            for token in freqs.keys():
                df_counter[token] += 1

        self.avg_doc_len = (total_words / len(chunks)) if chunks else 1.0
        n_docs = len(chunks)

        # Compute IDF
        for word, count in df_counter.items():
            self.idf[word] = math.log((n_docs - count + 0.5) / (count + 0.5) + 1.0)

        logger.info("BM25Retriever fit on %d document chunks.", len(chunks))

    def search(self, query: str, top_k: int = 5) -> List[Tuple[Dict[str, Any], float]]:
        """Search top-k chunks using BM25 scoring."""
        if not self.chunks:
            return []

        q_tokens = self._tokenize(query)
        scores = [0.0] * len(self.chunks)

        for i, freqs in enumerate(self.doc_freqs):
            dl = self.doc_len[i]
            score = 0.0
            for token in q_tokens:
                if token in freqs:
                    tf = freqs[token]
                    idf_val = self.idf.get(token, 0.0)
                    num = tf * (self.k1 + 1.0)
                    denom = tf + self.k1 * (1.0 - self.b + self.b * (dl / self.avg_doc_len))
                    score += idf_val * (num / denom)
            scores[i] = score

        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
        results = [(self.chunks[i], float(scores[i])) for i in top_indices if scores[i] > 0]
        return results
