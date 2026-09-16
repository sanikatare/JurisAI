# Slide 6: Machine Learning & Calibration

## Supervised Classification & Calibration
- **Candidate Model**: Random Forest Classifier (`v1.0.0`) with balanced class weights.
- **Performance**: Achieves **0.9231 PR-AUC**, **0.8421 Recall @ 1% FPR**, and **0.8889 F1 Score**.
- **Platt Calibration**: Logistic sigmoid recalibration mapping raw model confidence into calibrated probabilities (Brier Score = **0.0381**).
- **Cost-Sensitive Thresholding**: F1-optimal threshold selection at $0.2970$ operating point.
