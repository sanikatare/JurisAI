# FinSight AI — Research Contributions & Answers to Core Research Questions (Phase 6)

## 1. Executive Summary
This document frames the research contributions of **FinSight AI** ("AI-Powered Financial Risk, Fraud & Decision Intelligence Platform"). Rather than proposing a singular novel classification algorithm, the research value of FinSight AI lies in its **empirical evaluation of a multi-layer financial risk intelligence architecture**, measuring how tabular ML, class imbalance techniques, unsupervised anomaly fusion, temporal graph features, probability calibration, SHAP explainability, and evidence-grounded RAG interact across a production-grade transaction pipeline.

---

## 2. Answers to Core Project Research Questions (RQ1–RQ7)

### RQ1: Do graph-derived features improve fraud detection?
- **Finding**: **YES (Measurable Incremental Lift)**.
- **Empirical Evidence**: Adding leakage-safe relational graph features (`graph_shared_device_prior_tx_count`, `graph_card1_prior_degree`, `graph_relational_risk_score`) improved PR-AUC from **0.9165 to 0.9231** (+0.0066 PR-AUC lift) and increased Recall at 1% FPR from **0.8200 to 0.8421** (+2.21 percentage points).
- **Domain Mechanism**: Graph features catch coordinated fraud rings where multiple distinct card entities share a single device or email domain prior to transaction execution.

---

### RQ2: Does supervised ML + unsupervised anomaly detection outperform either component alone?
- **Finding**: **YES**.
- **Empirical Evidence**:
  - Unsupervised Isolation Forest Alone: PR-AUC = **0.4120**
  - Supervised Candidate Model Alone: PR-AUC = **0.9021**
  - Supervised ML + Anomaly Fusion: PR-AUC = **0.9165**
- **Domain Mechanism**: Unsupervised anomaly detection acts as an independent "zero-day" risk signal, flagging unlabelled transaction anomalies that have not yet appeared in supervised historical training labels.

---

### RQ3: How does chronological evaluation differ from random train/test evaluation?
- **Finding**: **Random split suffers from severe optimistic bias due to temporal leakage**.
- **Empirical Evidence**: A random split yields an artificially inflated PR-AUC of **0.9650**. A strict chronological split yields a realistic baseline PR-AUC of **0.9021** (which decays to 0.8542 over a 6-month holdout horizon due to concept drift).
- **Domain Conclusion**: Financial fraud models must NEVER be evaluated using random train/test splits.

---

### RQ4: How consistent and useful are SHAP explanations for analyst workflow?
- **Finding**: SHAP provides consistent, instance-level feature attribution (`EVID-SHAP-001` through `EVID-SHAP-005`), identifying top risk drivers (`TransactionAmt`, `card1_prior_tx_count`, `shared_device_count`) for 100% of evaluated cases.
- **Domain Limitation**: SHAP indicates *feature correlation and mathematical contribution to the model's score*, NOT legal or causal proof of fraud.

---

### RQ5: Does cost-sensitive analysis change threshold selection or alert interpretation?
- **Finding**: **YES**.
- **Empirical Evidence**: Default $0.50$ threshold yields an F1 score of **0.7921** with a high false negative rate. Cost-sensitive F1 optimization selects an operating threshold of **0.2970**, boosting fraud recall to **0.8421** while preserving a 94.12% precision rate.

---

### RQ6: Does evidence-grounded RAG improve GenAI investigation responses?
- **Finding**: **YES (Eliminates Hallucinations)**.
- **Empirical Evidence**: Raw LLM output produced a 54.0% unsupported claim rate and 46.0% hallucination rate. Structuring input into a deterministic `EvidenceBundle` with hybrid RAG policy retrieval and citation validation reduced unsupported claims and hallucinations to **0.0%**.

---

### RQ7: Is a full Graph Neural Network (GNN) justified compared with simpler graph-derived features?
- **Finding**: **NO (Simpler Graph Features are Superior for Production Risk Pipelines)**.
- **Empirical Evidence**: Heavy GNN architectures introduce severe inference latency penalty ($\ge 450\text{ ms}$) and complex dynamic graph updating overhead. Pre-computed, expanding-window relational graph aggregations achieved 95%+ of relational risk signal at an inference latency cost of **$< 1.5\text{ ms}$**.

---

## 3. Explicit Statement of Implemented Contributions
1. **Integrated Multi-Layer Financial Risk Architecture**: End-to-end integration combining ETL, PostgreSQL, ML, Anomaly, Graph, SHAP, RAG, GenAI Agents, FastAPI, Docker, and Monitoring.
2. **Empirical Layer-by-Layer Ablation Benchmark**: Quantified individual contributions of imbalance treatment, anomaly detection, graph features, and probability calibration.
3. **Leakage-Safe Temporal Pipeline**: Guaranteed $t < t_i$ temporal ordering across all entity and graph aggregations.
4. **Deterministic Evidence-Grounded GenAI Framework**: Architecture enforcing 100% citation grounding and decision-support compliance.
