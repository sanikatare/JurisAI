# Slide 7: Unsupervised Anomaly Detection

## Zero-Day Anomaly Fusion
- **Model**: Unsupervised Isolation Forest trained on normal behavior baselines.
- **Role**: Computes independent `anomaly_score` for incoming transactions.
- **Value Add**: Captures novel, unlabelled fraud patterns that have not yet appeared in supervised training data, adding +0.0055 PR-AUC lift when fused with supervised model scores.
