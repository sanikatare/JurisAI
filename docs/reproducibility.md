# FinSight AI — Reproducibility Specification

## 1. Overview
Full end-to-end reproducibility is guaranteed across feature engineering, chronological splitting, model training, threshold selection, probability calibration, and experiment reporting.

---

## 2. Reproducibility Configuration Matrix

| Parameter / Layer | Setting / Seed | Governing Configuration File |
|---|---|---|
| **Random Seed** | `42` | `configs/ml_config.yaml` (`split.random_seed`, `models.*.random_state`) |
| **Chronological Split Ratio** | `60% Train / 20% Val / 20% Test` | `configs/config.yaml` (`temporal:` section) |
| **Numeric Imputation Strategy** | `Median + _was_missing indicator` | `src/ml/preprocessing.py` |
| **Categorical Encoding Strategy** | `Frequency (High-card) / OneHot (Low-card)` | `src/ml/preprocessing.py` |
| **Imbalance Strategy** | `Class Weighting (balanced)` | `src/ml/train.py` |
| **Probability Calibration** | `Platt Scaling (Sigmoid)` | `src/ml/calibration.py` |
| **Optimal Threshold Selection** | `Max F1 (0.2970)` | `src/ml/threshold.py` |

---

## 3. How to Reproduce All Phase 3 & 4 Experiments

```bash
# 1. Activate environment & install requirements
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. Execute Master Experiment Pipeline (Synthetic or Real Mode)
python -m src.ml.experiment_runner --synthetic

# 3. Execute Pytest Verification Pyramid
pytest tests/ -v
```
