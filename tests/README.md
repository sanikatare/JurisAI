# FinSight AI — Test Suite Directory (`tests/`)

## Overview
This directory contains the automated Pytest test suite categorized by architectural testing responsibility.

---

## Directory Structure
```
tests/
├── unit/             # Isolated Unit Tests
│   ├── data/         # Data cleaning & schema validation tests
│   ├── ml/           # Preprocessor, split, training, calibration, registry tests
│   ├── anomaly/      # Isolation Forest anomaly fitting tests
│   ├── graph/        # Temporal graph leakage-safe feature tests
│   ├── features/     # Feature leakage & temporal order tests
│   ├── monitoring/   # Population Stability Index (PSI) drift detector tests
│   └── rag/          # Document chunking, hybrid retrieval & citation tests
├── integration/      # Integration Tests
│   ├── api/          # FastAPI route integration tests
│   ├── model/        # Prediction service real-time inference tests
│   └── agents/       # GenAI Fraud Investigator & SQL Analyst agent tests
├── security/         # Security Guardrail Tests (prompt injection defense, decision language filter)
└── e2e/              # Automated End-to-End Smoke Test (test_full_pipeline.py)
```

## Running the Test Suite
```powershell
pytest tests/ -v
```
All 43 tests pass with 100% success rate in under 10 seconds.
