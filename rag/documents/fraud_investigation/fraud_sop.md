# Financial Fraud Investigation Standard Operating Procedure

**Document ID**: `POL-FRAUD-2026-v1`  
**Category**: Fraud Investigation  
**Source**: Financial Risk & Operations Manual  
**Effective Date**: February 2026  

## 1. Risk Tier Framework
- **Low Risk ($\text{Score} < 0.30$)**: Auto-cleared for processing unless explicit velocity rules trigger.
- **Medium Risk ($0.30 \le \text{Score} < 0.70$)**: Flagged for analyst queue; requires manual inspection of SHAP top feature drivers.
- **High Risk ($\text{Score} \ge 0.70$)**: Priority investigation required. Analyst must compile full Evidence Bundle and review RAG policy guidance.

## 2. SHAP & Explainability Guidance
- Feature contributions from `TransactionAmt` and `C1-C14` counts indicate transaction scale anomalies.
- Positive SHAP values increase predicted fraud risk; negative values push the prediction toward legitimate status.
- Analysts must verify whether SHAP feature drivers align with historical customer behavior before escalating.

## 3. Evidence Traceability Requirement
All investigation narratives and formal reports must include exact evidence IDs for:
- Calibrated ML Probability (`[ML-001]`)
- Top SHAP Feature Contributions (`[SHAP-001]`, `[SHAP-002]`)
- Graph Relational Degree (`[GRAPH-001]`)
- Policy SOP Citations (`[RAG-001]`)
