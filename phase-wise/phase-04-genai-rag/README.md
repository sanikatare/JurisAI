# Phase 4 — Generative AI, RAG & Investigation Intelligence

## Overview
Phase 4 established the GenAI intelligence layer on top of computed ML evidence. It introduced deterministic Evidence Bundles, Hybrid RAG policy retrieval (FAISS + BM25 with Reciprocal Rank Fusion), `FraudInvestigatorAgent`, `ReportingAgent`, `DataAnalystAgent`, and prompt/citation safety guardrails.

---

## Documents & Reports
- **[phase4-completion-report.md](./phase4-completion-report.md)**: Overview of Phase 4 GenAI & RAG implementation.
- **[rag-architecture.md](./rag-architecture.md)**: Architecture blueprint for hybrid RAG retrieval and citation validation.
- **[evidence-bundle.md](./evidence-bundle.md)**: Specification of deterministic `EvidenceBundle` structure.
- **[retrieval.md](./retrieval.md)**: Reciprocal Rank Fusion (RRF) dense + lexical search methodology.
- **[fraud-investigator-agent.md](./fraud-investigator-agent.md)**: Primary case investigation agent prompt design and guardrails.
- **[data-analyst-agent.md](./data-analyst-agent.md)**: Read-only SQL agent safety validator.
- **[reporting-agent.md](./reporting-agent.md)**: Executive Markdown compliance report generator.
- **[guardrails.md](./guardrails.md)**: Prompt injection and decision language safety filters.
- **[citation-enforcement.md](./citation-enforcement.md)**: Automated citation extraction and grounding verification.
- **[genai-evaluation.md](./genai-evaluation.md)**: Scientific evaluation benchmark comparing 4 GenAI setups.
