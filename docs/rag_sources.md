# RAG Knowledge Base Manifest & Source Documentation

| Document File | Document ID | Title / Topic | Category | Version | Purpose | Limitations |
|---|---|---|---|---|---|---|
| `knowledge_base/aml/aml_sop.md` | `POL-AML-2026-v1` | AML & Suspicious Activity Investigation SOP | AML Compliance | v1.0 (Jan 2026) | Guidance on device sharing & velocity risk | Representative SOP for academic research |
| `knowledge_base/kyc/kyc_compliance.md` | `POL-KYC-2026-v1` | Customer Identification & KYC Risk Guidelines | KYC Compliance | v1.0 (Jan 2026) | Verification of missing identity metadata & high amount risk | Representative guidelines |
| `knowledge_base/fraud_investigation/fraud_sop.md` | `POL-FRAUD-2026-v1` | Financial Fraud Investigation SOP | Fraud Operations | v1.0 (Feb 2026) | Risk tier definitions, SHAP interpretations, citation rules | Internal operations manual |
| `knowledge_base/risk_management/risk_policy.md` | `POL-RISK-2026-v1` | Enterprise Financial Risk Management & Decision Policy | Risk Management | v1.0 (Jan 2026) | Cost-sensitive thresholds & decision authority governance | Governance policy |

---

## Usage Notes
- Documents are chunked into 300–500 token sliding windows with metadata headers preserved.
- Citations (`[RAG-001]`, `[RAG-002]`) link generated claims directly to chunk IDs.
