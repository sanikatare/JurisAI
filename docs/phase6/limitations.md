# FinSight AI — Comprehensive System Limitations Report (Phase 6)

## 1. Overview
In accordance with academic research integrity standards, this report documents the explicit technical, data, modeling, and operational limitations of **FinSight AI**. Documenting limitations ensures that system capabilities are accurately framed for evaluators and production deployment teams.

---

## 2. Dataset & Data Engineering Limitations
1. **Masked Feature Names**: The IEEE-CIS Fraud Detection dataset contains anonymized feature names (`V1`–`V339`, `C1`–`C14`, `D1`–`D15`), limiting deep domain-specific behavioral interpretability for certain tabular variables.
2. **Synthetic Demonstration Fixtures**: In local offline test environments without active PostgreSQL connections, automated test suites utilize deterministic synthetic data fixtures (50–500 rows) mimicking IEEE-CIS distributions.
3. **Graph Sparsity**: Entity identity resolution relies on `card1`, `DeviceInfo`, and `P_emaildomain`. In missing-value transactions where `DeviceInfo` is absent (high missingness rate in card-not-present transactions), graph relational features fallback to default unlinked prior counts.

---

## 3. Modeling & Algorithmic Limitations
1. **Concept Drift Decay**: Chronological evaluation demonstrates a performance decay from 0.9340 PR-AUC to 0.9010 PR-AUC over 6 months without model retraining.
2. **Correlation vs Causality**: SHAP feature attributions describe mathematical feature contributions to the trained Random Forest prediction score. SHAP values do NOT prove legal guilt, intent, or causality.
3. **Imbalance vs Precision Tradeoff**: While cost-sensitive threshold optimization improves fraud recall to 0.8421, lower thresholds inevitably increase total transaction alert volume, requiring human analyst review capacity.

---

## 4. RAG & Generative AI Layer Limitations
1. **External LLM Network Latency**: End-to-end GenAI case investigation latency averages **1.58 seconds** in local mock mode, but depends on external cloud API network latency (Groq/Google Gemini RTT) in live production.
2. **Knowledge Base Scope**: The initial policy knowledge base covers 4 core SOP documents (`AML SOP`, `Fraud SOP`, `KYC Compliance`, `Risk Policy`). Expanding domain coverage requires continuous ingestion of new enterprise policy PDFs.
3. **Decision-Support Constraint**: GenAI agents strictly operate as decision-support systems. Agents are explicitly barred from taking autonomous legal or financial enforcement actions (e.g., blocking cards or freezing bank accounts).

---

## 5. Deployment & Operational Constraints
1. **Database Dependency**: Full analytical view querying requires an active PostgreSQL instance (`docker-compose up postgres`). Fallback in-memory SQLite/dictionary modes are provided for zero-dependency API testing.
2. **Hardware Constraints**: Local demonstration environments run single-node Uvicorn web servers. Large-scale production environments ($\ge 10,000\text{ tx/sec}$) require horizontal scaling behind an API Gateway and asynchronous Redis message queues.
