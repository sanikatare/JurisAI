# Slide 13: Experimental Design & Setup

## Scientific Methodology
- **Dataset**: IEEE-CIS Financial Fraud Detection (590,540 transactions).
- **Split Protocol**: Chronological split (70% train / 15% val / 15% test).
- **Primary Metric**: Precision-Recall AUC (PR-AUC) and Recall at 1% FPR.
- **Secondary Metrics**: ROC-AUC, Precision, Recall, F1 Score, Brier Score, Latency (ms).
- **Ablation Protocol**: Layer-by-layer evaluation isolating ML, Imbalance, Anomaly, Graph, Calibration, SHAP, and RAG/GenAI.
