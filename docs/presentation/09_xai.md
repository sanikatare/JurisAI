# Slide 9: Explainable AI (SHAP)

## Instance-Level Model Transparency
- **Framework**: TreeSHAP feature explainer (`TransactionSHAPExplainer`).
- **Function**: Extracts top $k$ positive (risk-increasing) and negative (risk-decreasing) feature attributions per transaction.
- **Output**: Generates structured citations (`EVID-SHAP-001` through `EVID-SHAP-005`) for evidence bundle integration.
- **Analyst Benefit**: Replaces opaque predictions with human-understandable risk drivers.
