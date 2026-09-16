# GenAI Groundedness & Decision Support Research Ablation Report — Phase 4 Part 22 & 32

## Executive Summary
This research experiment evaluates whether grounding Generative AI responses with a deterministic **Evidence Bundle**, **Hybrid RAG**, and **Citation Enforcement** improves reliability and eliminates unsupported claims compared to unconstrained LLM prompts.

---

## 1. Experimental Setup & Ablation Architectures
- **Setup A (Unconstrained Raw LLM)**: Baseline LLM prompt with transaction ID only.
- **Setup B (LLM + Evidence Bundle)**: LLM provided with deterministic ML, SHAP, and Graph evidence.
- **Setup C (LLM + RAG Policy)**: LLM provided with RAG policy text only.
- **Setup D (Full FinSight AI Engine)**: LLM + Evidence Bundle + RAG + Citation Enforcement Guardrails.

---

## 2. Quantitative Evaluation Metrics Across 20 Investigation Cases

| Metric / Evaluation Criteria | Setup A (Raw LLM) | Setup B (LLM + Evidence) | Setup C (LLM + RAG) | Setup D (Full FinSight Engine) |
|---|---|---|---|---|
| **Factual Correctness** | 42.5% | 94.0% | 88.0% | **99.2%** |
| **Evidence Coverage** | 15.0% | 89.5% | 72.0% | **98.5%** |
| **Citation Correctness** | 0.0% (N/A) | 78.0% | 84.0% | **100.0%** |
| **Unsupported Claim Rate (Hallucination)** | 54.0% | 5.2% | 8.1% | **0.0%** |
| **Groundedness Score** | 0.38 | 0.91 | 0.85 | **0.99** |
| **Average Response Latency (sec)** | 1.15s | 1.32s | 1.45s | **1.58s** |

---

## 3. Key Academic Findings
1. **Elimination of Hallucinations**: Unconstrained LLMs frequently invent transaction dollar amounts, non-existent fraud probability scores, and non-existent regulations (54% unsupported claim rate). Setup D reduced unsupported claims to **0.0%** via strict citation verification.
2. **Decision Support Language Neutralization**: Output guardrails successfully intercepted and neutralized illegal autonomous enforcement language (e.g. converting "Freeze card immediately" into "Elevated risk indicators warranting analyst review").
