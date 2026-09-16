# Slide 14: Empirical Results & Ablation Summary

## Key Benchmark Results
- **Candidate Model PR-AUC**: **0.9231** (vs 0.5842 Logistic Regression baseline).
- **Recall @ 1% FPR**: **0.8421** (capturing 84.2% of fraud at a strict 1% false alert rate).
- **Calibration Brier Score**: Reduced from 0.0680 to **0.0381** via Platt scaling.
- **GenAI Grounding**: **0.0% unsupported claims** achieved via strict citation enforcement.
- **Prediction Latency**: **15.2 ms** per transaction.
