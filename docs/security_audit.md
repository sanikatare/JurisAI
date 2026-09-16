# FinSight AI — Security Audit & Threat Model Specification

## 1. Executive Summary
This document provides the security audit, threat model, and defense specification for FinSight AI across API, Database, ML, and GenAI layers.

---

## 2. Threat Matrix & Defensive Controls

| Threat Category | Attack Vector | Risk Level | Defensive Control & Implementation | Verification |
|---|---|---|---|---|
| **API Vulnerabilities** | Prompt Injection via query string | **High** | Regex pattern matching (`check_input_prompt_injection` in `src/genai/guardrails.py`) | `test_check_input_prompt_injection` |
| | Unauthenticated bulk endpoint access | **Medium** | API Key header validation middleware (`X-API-Key` check in `src/api/app.py`) | `test_api_production.py` |
| | Denial of Service / Resource Exhaustion | **Medium** | Rate limiting middleware + max token generation caps | `src/config.py` settings |
| **SQL Injection** | Malicious SQL in Data Analyst Agent | **Critical** | AST/Regex read-only safety parser enforcing `SELECT` only (`validate_sql_safety`) | `test_sql_safety_validator_rejects_dml_ddl` |
| **Data Leakage** | Target or future information in ML features | **Critical** | Chronological split + `.shift(1)` expanding windows + 10-point ML leakage audit | `docs/ml_leakage_audit.md` |
| **GenAI Hallucination** | Autonomous illegal enforcement recommendations | **High** | Decision language filter replacing "freeze/block" with neutral decision support language | `test_sanitize_output_decision_language` |
| **Secret Exposure** | Hardcoded API keys committed in git | **Critical** | `.gitignore` + `.env` environment loading (`src/config.py`) | Repository git audit |
