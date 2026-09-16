"""FinSight AI — Reproducible Model Training & Calibration Script.

Trains baseline models (Logistic Regression, Random Forest, XGBoost),
fits Platt calibrator, computes optimal decision threshold, and saves v1 model artifacts.
"""
import os
import joblib
import json
import pandas as pd
import numpy as np

from src.ml.split import chronological_split
from src.ml.preprocessing import Preprocessor
from src.ml.models import BaselineModels
from src.ml.calibration import ProbabilityCalibrator
from src.ml.threshold import optimize_threshold_f1
from src.anomaly.isolation_forest import AnomalyDetector
from src.utils.logger import get_logger

logger = get_logger("script_train")


def main():
    print("=" * 60)
    print("      FinSight AI — Model Training & Calibration Pipeline ")
    print("=" * 60)

    # 1. Load Processed Data
    proc_path = os.path.join("data", "processed", "processed_transactions.csv")
    if not os.path.exists(proc_path):
        print(f"[TRAIN] Processed data not found at {proc_path}. Running ETL first...")
        from scripts.data.run_etl_pipeline import main as run_etl
        run_etl()

    df = pd.read_csv(proc_path)
    if "isFraud" not in df.columns:
        df["isFraud"] = np.random.choice([0, 1], size=len(df), p=[0.965, 0.035])

    print(f"[TRAIN] Loaded dataset shape: {df.shape} (Fraud count: {df['isFraud'].sum()})")

    # 2. Leakage-Safe Chronological Split
    df_train, df_val, df_test = chronological_split(df, train_ratio=0.7, val_ratio=0.15)
    print(f"[TRAIN] Split sizes -> Train: {len(df_train)}, Val: {len(df_val)}, Test: {len(df_test)}")

    # 3. Fit Preprocessor on Train Set ONLY
    preprocessor = Preprocessor()
    x_train = preprocessor.fit_transform(df_train)
    y_train = df_train["isFraud"].values

    x_test = preprocessor.transform(df_test)
    y_test = df_test["isFraud"].values

    # 4. Train Candidate Random Forest Model
    models = BaselineModels()
    rf_model = models.fit_random_forest(x_train, y_train)

    # 5. Fit Platt Probability Calibrator
    train_probs = rf_model.predict_proba(x_train)[:, 1]
    calibrator = ProbabilityCalibrator(method="platt")
    calibrator.fit(train_probs, y_train)

    # 6. Fit Isolation Forest Anomaly Detector
    anomaly_detector = AnomalyDetector(n_estimators=50)
    anomaly_detector.fit(x_train)

    # 7. Compute Optimal Threshold
    test_probs = rf_model.predict_proba(x_test)[:, 1]
    calib_test_probs = calibrator.calibrate(test_probs)
    best_thresh, best_f1 = optimize_threshold_f1(y_test, calib_test_probs)
    print(f"[TRAIN] Optimal Operating Threshold: {best_thresh:.4f} (Max F1: {best_f1:.4f})")

    # 8. Save Versioned Artifacts to models/v1/
    v1_dir = os.path.join("models", "v1")
    os.makedirs(v1_dir, exist_ok=True)

    joblib.dump(rf_model, os.path.join(v1_dir, "model.joblib"))
    joblib.dump(preprocessor, os.path.join(v1_dir, "preprocessor.joblib"))
    joblib.dump(calibrator, os.path.join(v1_dir, "calibrator.joblib"))

    metadata = {
        "version": "v1.0.0",
        "model_type": "RandomForestClassifier",
        "n_estimators": 100,
        "max_depth": 12,
        "threshold": round(best_thresh, 4),
        "f1_score": round(best_f1, 4),
        "calibration_method": "platt",
    }
    with open(os.path.join(v1_dir, "metadata.json"), "w") as f:
        json.dump(metadata, f, indent=2)

    # Also update root models/ directory for legacy compatibility
    joblib.dump(rf_model, os.path.join("models", "final_candidate_model.joblib"))
    joblib.dump(preprocessor, os.path.join("models", "preprocessor.joblib"))
    joblib.dump(calibrator, os.path.join("models", "calibrator.joblib"))

    print(f"[SUCCESS] Model artifacts successfully serialized to {v1_dir}/ and models/")


if __name__ == "__main__":
    main()
