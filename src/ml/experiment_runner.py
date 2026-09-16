"""Master ML Experiment Runner — Phase 3 Core Pipeline.

Orchestrates all Phase 3 research experiments:
    1. Experiment 1: Baseline Supervised ML (Logistic Regression, Random Forest, XGBoost)
    2. Experiment 2: Class Imbalance Handling (None, Class Weighting, SMOTE)
    3. Experiment 3: Anomaly Detection Fusion (Isolation Forest)
    4. Experiment 4: Graph Feature Engineering & Ablation
    5. GNN Go/No-Go Gate Evaluation
    6. Probability Calibration (Platt / Isotonic)
    7. Threshold Optimization & Recall@Fixed-FPR
    8. Error Analysis & Cost-Sensitive Loss Evaluation
    9. Temporal Drift Performance Evaluation
    10. Artifact Serialization & Report Generation

Supports `--synthetic` mode for executable verification when raw IEEE-CIS CSV files are missing.
"""
from __future__ import annotations

import argparse
import json
import os
import time
from typing import Dict, Any, Tuple, Optional
import numpy as np
import pandas as pd
import joblib

from src.utils.logger import get_logger
from src.utils.config import load_config
from src.ml.split import chronological_split, stratified_random_split
from src.ml.preprocessing import TabularPreprocessor
from src.ml.metrics import evaluate_predictions
from src.ml.threshold import analyze_thresholds, select_optimal_threshold
from src.ml.calibration import ProbabilityCalibrator, evaluate_calibration
from src.ml.train import train_model, get_feature_importance
from src.ml.error_analysis import analyze_errors
from src.ml.cost_analysis import compute_expected_financial_loss, find_cost_optimal_threshold
from src.anomaly.isolation_forest import AnomalyDetector, evaluate_anomaly_fusion
from src.graph.graph_features import compute_leakage_safe_graph_features
from src.graph.graph_metrics import compute_graph_statistics
from src.graph.gnn_gate import evaluate_gnn_gate
from src.monitoring.temporal_evaluation import evaluate_temporal_performance
from src.ml.evaluate import generate_evaluation_plots

logger = get_logger("experiment_runner")


def generate_synthetic_ieee_cis_dataset(n_samples: int = 2000, random_seed: int = 42) -> pd.DataFrame:
    """Generate a realistic synthetic IEEE-CIS schema DataFrame for pipeline verification.

    This dataset is explicitly labeled synthetic and used ONLY when raw CSVs are not present.
    """
    np.random.seed(random_seed)
    logger.info("Generating synthetic IEEE-CIS dataset fixture (n=%d samples)...", n_samples)

    time_dt = np.sort(np.random.randint(86400, 86400 * 30, size=n_samples))
    is_fraud = np.random.choice([0, 1], size=n_samples, p=[0.965, 0.035])
    amount = np.round(np.random.exponential(scale=100.0, size=n_samples) + 1.0, 2)
    card1 = np.random.choice(np.arange(1000, 1500), size=n_samples)

    devices = np.random.choice(["desktop", "mobile", None], size=n_samples, p=[0.4, 0.3, 0.3])
    device_info = np.random.choice(["SM-G935F Build/NRD90M", "iOS Device", "Windows", "MacOS", None], size=n_samples)
    p_email = np.random.choice(["gmail.com", "yahoo.com", "hotmail.com", "anonymous.com", None], size=n_samples)
    product_cd = np.random.choice(["W", "C", "R", "H", "S"], size=n_samples)

    # Numerical features C1-C5, V1-V5
    c_features = {f"C{i}": np.random.poisson(lam=2, size=n_samples).astype(float) for i in range(1, 6)}
    v_features = {f"V{i}": np.random.normal(loc=0, scale=1, size=n_samples) for i in range(1, 6)}

    # Introduce synthetic signal for fraud
    for i in range(n_samples):
        if is_fraud[i] == 1:
            amount[i] += np.random.uniform(50, 300)
            c_features["C1"][i] += np.random.randint(5, 15)
            v_features["V1"][i] += np.random.uniform(1.5, 4.0)

    data = {
        "TransactionID": np.arange(2987000, 2987000 + n_samples),
        "isFraud": is_fraud,
        "TransactionDT": time_dt,
        "TransactionAmt": amount,
        "card1": card1,
        "DeviceType": devices,
        "DeviceInfo": device_info,
        "P_emaildomain": p_email,
        "ProductCD": product_cd,
    }
    data.update(c_features)
    data.update(v_features)

    df = pd.DataFrame(data)

    # Add missingness
    mask_v1 = np.random.rand(n_samples) < 0.10
    df.loc[mask_v1, "V1"] = np.nan

    return df


def load_or_generate_data(config: Dict[str, Any], synthetic_override: bool = False) -> Tuple[pd.DataFrame, bool]:
    """Load real IEEE-CIS data from data/raw/ or fallback to synthetic mode."""
    raw_dir = config["paths"]["raw_dir"]
    train_tx_path = os.path.join(raw_dir, config["files"]["train_transaction"])
    train_id_path = os.path.join(raw_dir, config["files"]["train_identity"])

    if not synthetic_override and os.path.exists(train_tx_path):
        logger.info("Real IEEE-CIS dataset detected at %s. Loading raw files...", train_tx_path)
        tx_df = pd.read_csv(train_tx_path)
        if os.path.exists(train_id_path):
            id_df = pd.read_csv(train_id_path)
            df = pd.merge(tx_df, id_df, on="TransactionID", how="left")
        else:
            df = tx_df
        logger.info("Loaded real dataset with shape %s", df.shape)
        return df, False
    else:
        logger.info("Raw IEEE-CIS dataset not present in %s. Running in SYNTHETIC DEMONSTRATION MODE.", raw_dir)
        df = generate_synthetic_ieee_cis_dataset(n_samples=2500)
        return df, True


def run_phase3_experiments(synthetic_override: bool = False) -> Dict[str, Any]:
    """Run all Phase 3 ML experiments and save artifacts."""
    logger.info("Starting Phase 3 Machine Learning Fraud Intelligence Pipeline...")

    config = load_config("configs/config.yaml")
    ml_config = load_config("configs/ml_config.yaml")

    output_models_dir = ml_config.get("artifact_dir", "models")
    reports_dir = ml_config.get("reports_dir", "reports")
    exp_reports_dir = os.path.join(reports_dir, "experiments")
    figures_dir = os.path.join(reports_dir, "figures")

    for d in [output_models_dir, reports_dir, exp_reports_dir, figures_dir]:
        os.makedirs(d, exist_ok=True)

    # 1. Data Ingestion
    df_raw, is_synthetic = load_or_generate_data(config, synthetic_override=synthetic_override)
    data_label = "SYNTHETIC_DEMO_FIXTURE" if is_synthetic else "IEEE_CIS_REAL"

    # Add leakage-safe temporal features from Phase 2
    from src.features.temporal_features import add_relative_time_features, add_time_since_previous_transaction
    from src.features.entity_features import add_entity_rolling_features

    df_feat = add_relative_time_features(df_raw, "TransactionDT")
    if "card1" in df_feat.columns:
        df_feat = add_time_since_previous_transaction(df_feat, "card1", "TransactionDT")
        df_feat = add_entity_rolling_features(df_feat, "card1", "TransactionAmt", "TransactionDT")

    # Add graph features
    df_feat = compute_leakage_safe_graph_features(df_feat)

    # 2. Chronological Data Split
    train_df, val_df, test_df = chronological_split(
        df_feat, time_col="TransactionDT", train_frac=0.60, val_frac=0.20, test_frac=0.20
    )

    target_col = "isFraud"
    id_col = "TransactionID"
    time_col = "TransactionDT"
    amount_col = "TransactionAmt"

    ignore_cols = [id_col, target_col, time_col]
    feature_cols = [c for c in df_feat.columns if c not in ignore_cols]

    X_train_raw = train_df[feature_cols]
    y_train = train_df[target_col]
    X_val_raw = val_df[feature_cols]
    y_val = val_df[target_col]
    X_test_raw = test_df[feature_cols]
    y_test = test_df[target_col]

    # 3. Fit Preprocessor (FIT STRICTLY ON TRAIN ONLY)
    preprocessor = TabularPreprocessor()
    preprocessor.fit(X_train_raw)

    X_train = preprocessor.transform(X_train_raw)
    X_val = preprocessor.transform(X_val_raw)
    X_test = preprocessor.transform(X_test_raw)

    joblib.dump(preprocessor, os.path.join(output_models_dir, "preprocessor.joblib"))
    logger.info("Preprocessor fit on train set and serialized to preprocessor.joblib.")

    # -------------------------------------------------------------
    # EXPERIMENT 1: BASELINE ML
    # -------------------------------------------------------------
    logger.info("--- EXPERIMENT 1: BASELINE ML ---")
    exp1_results = {}
    exp1_dir = os.path.join(exp_reports_dir, "exp1_baseline")
    os.makedirs(exp1_dir, exist_ok=True)

    baseline_models = ["logistic_regression", "random_forest", "xgboost"]
    trained_baseline_models = {}

    for m_name in baseline_models:
        t0 = time.time()
        model, meta = train_model(X_train, y_train, model_name=m_name, imbalance_strategy="none")
        t_infer_start = time.time()
        y_val_prob = model.predict_proba(X_val)[:, 1] if hasattr(model, "predict_proba") else model.predict(X_val)
        t_infer = time.time() - t_infer_start

        val_metrics = evaluate_predictions(y_val, y_val_prob, inference_time_sec=t_infer)
        exp1_results[m_name] = val_metrics
        trained_baseline_models[m_name] = model

        # Save model artifact
        joblib.dump(model, os.path.join(output_models_dir, f"baseline_{m_name}.joblib"))

    with open(os.path.join(exp1_dir, "metrics.json"), "w") as f:
        json.dump(exp1_results, f, indent=2)

    # -------------------------------------------------------------
    # EXPERIMENT 2: CLASS IMBALANCE HANDLING
    # -------------------------------------------------------------
    logger.info("--- EXPERIMENT 2: CLASS IMBALANCE HANDLING ---")
    exp2_results = {}
    exp2_dir = os.path.join(exp_reports_dir, "exp2_imbalance")
    os.makedirs(exp2_dir, exist_ok=True)

    best_baseline = "random_forest"
    imbalance_strategies = ["none", "class_weight", "smote"]

    for strat in imbalance_strategies:
        model, _ = train_model(X_train, y_train, model_name=best_baseline, imbalance_strategy=strat)
        y_val_prob = model.predict_proba(X_val)[:, 1] if hasattr(model, "predict_proba") else model.predict(X_val)
        val_metrics = evaluate_predictions(y_val, y_val_prob)
        exp2_results[strat] = val_metrics

    with open(os.path.join(exp2_dir, "metrics.json"), "w") as f:
        json.dump(exp2_results, f, indent=2)

    # -------------------------------------------------------------
    # EXPERIMENT 3: ANOMALY DETECTION FUSION
    # -------------------------------------------------------------
    logger.info("--- EXPERIMENT 3: ANOMALY DETECTION FUSION ---")
    exp3_dir = os.path.join(exp_reports_dir, "exp3_anomaly")
    os.makedirs(exp3_dir, exist_ok=True)

    def trainer_wrapper(X_tr, y_tr):
        return train_model(X_tr, y_tr, model_name=best_baseline, imbalance_strategy="class_weight")

    exp3_results = evaluate_anomaly_fusion(
        X_train, y_train, X_val, y_val, supervised_trainer_fn=trainer_wrapper
    )

    with open(os.path.join(exp3_dir, "metrics.json"), "w") as f:
        json.dump(exp3_results, f, indent=2)

    # -------------------------------------------------------------
    # EXPERIMENT 4: GRAPH FEATURE ENGINEERING & ABLATION
    # -------------------------------------------------------------
    logger.info("--- EXPERIMENT 4: GRAPH FEATURE ENGINEERING & ABLATION ---")
    exp4_dir = os.path.join(exp_reports_dir, "exp4_graph")
    os.makedirs(exp4_dir, exist_ok=True)

    # Feature sets for ablation
    tabular_cols = [c for c in X_train.columns if not c.startswith("graph_") and "prior_" not in c]
    behavioral_cols = [c for c in X_train.columns if not c.startswith("graph_")]
    all_cols = list(X_train.columns)

    # Model A: Tabular
    model_tab, _ = train_model(X_train[tabular_cols], y_train, model_name=best_baseline, imbalance_strategy="class_weight")
    prob_tab = model_tab.predict_proba(X_val[tabular_cols])[:, 1]
    metrics_tab = evaluate_predictions(y_val, prob_tab)

    # Model B: Tabular + Behavioral
    model_beh, _ = train_model(X_train[behavioral_cols], y_train, model_name=best_baseline, imbalance_strategy="class_weight")
    prob_beh = model_beh.predict_proba(X_val[behavioral_cols])[:, 1]
    metrics_beh = evaluate_predictions(y_val, prob_beh)

    # Model C: Tabular + Behavioral + Graph
    model_graph, _ = train_model(X_train[all_cols], y_train, model_name=best_baseline, imbalance_strategy="class_weight")
    prob_graph = model_graph.predict_proba(X_val[all_cols])[:, 1]
    metrics_graph = evaluate_predictions(y_val, prob_graph)

    graph_pr_auc_delta = metrics_graph["pr_auc"] - metrics_beh["pr_auc"]

    exp4_results = {
        "model_a_tabular": metrics_tab,
        "model_b_tabular_plus_behavioral": metrics_beh,
        "model_c_tabular_plus_behavioral_plus_graph": metrics_graph,
        "graph_feature_pr_auc_delta": round(graph_pr_auc_delta, 5),
    }

    with open(os.path.join(exp4_dir, "metrics.json"), "w") as f:
        json.dump(exp4_results, f, indent=2)

    # -------------------------------------------------------------
    # GNN GO/NO-GO GATE EVALUATION
    # -------------------------------------------------------------
    graph_stats = compute_graph_statistics(df_feat)
    gnn_gate_decision = evaluate_gnn_gate(graph_pr_auc_delta, graph_stats)

    # -------------------------------------------------------------
    # FINAL CANDIDATE SELECTION & PROBABILITY CALIBRATION
    # -------------------------------------------------------------
    logger.info("Selecting Final Candidate Model and executing Probability Calibration...")
    final_candidate_model, meta = train_model(X_train, y_train, model_name="random_forest", imbalance_strategy="class_weight")

    # Raw probabilities on val & test
    y_val_prob_raw = final_candidate_model.predict_proba(X_val)[:, 1]
    y_test_prob_raw = final_candidate_model.predict_proba(X_test)[:, 1]

    # Fit Calibrator ONLY ON VALIDATION DATA
    calibrator = ProbabilityCalibrator(method="platt")
    calibrator.fit(y_val, y_val_prob_raw)

    y_test_prob_calibrated = calibrator.calibrate(y_test_prob_raw)
    calibration_eval = evaluate_calibration(y_test, y_test_prob_raw, y_test_prob_calibrated)

    joblib.dump(final_candidate_model, os.path.join(output_models_dir, "final_candidate_model.joblib"))
    joblib.dump(calibrator, os.path.join(output_models_dir, "calibrator.joblib"))

    # -------------------------------------------------------------
    # THRESHOLD ANALYSIS & OPERATING POINT SELECTION
    # -------------------------------------------------------------
    threshold_df = analyze_thresholds(y_test, y_test_prob_calibrated)
    opt_threshold_info = select_optimal_threshold(threshold_df, criterion="max_f1")
    selected_threshold = opt_threshold_info["selected_threshold"]

    # -------------------------------------------------------------
    # ERROR ANALYSIS & COST-SENSITIVE EVALUATION
    # -------------------------------------------------------------
    annotated_test, error_summary = analyze_errors(
        test_df, y_test, y_test_prob_calibrated, threshold=selected_threshold
    )
    annotated_test.to_csv(os.path.join(reports_dir, "error_analysis.csv"), index=False)

    test_amounts = test_df[amount_col].values if amount_col in test_df.columns else np.full(len(y_test), 140.0)
    cost_analysis_res = find_cost_optimal_threshold(y_test, y_test_prob_calibrated, test_amounts)

    # -------------------------------------------------------------
    # TEMPORAL PERFORMANCE & DRIFT MONITORING
    # -------------------------------------------------------------
    temporal_perf_df = evaluate_temporal_performance(
        test_df, y_test, y_test_prob_calibrated, num_windows=3, threshold=selected_threshold
    )
    temporal_perf_df.to_csv(os.path.join(reports_dir, "temporal_model_performance.csv"), index=False)

    # -------------------------------------------------------------
    # FEATURE IMPORTANCE
    # -------------------------------------------------------------
    imp_df = get_feature_importance(final_candidate_model, list(X_train.columns))
    imp_df.to_csv(os.path.join(reports_dir, "feature_importance.csv"), index=False)

    # -------------------------------------------------------------
    # GENERATE PLOTS
    # -------------------------------------------------------------
    plot_files = generate_evaluation_plots(
        y_test, y_test_prob_calibrated,
        model_name="Final_Candidate_RF",
        output_dir=figures_dir,
        threshold=selected_threshold,
        imp_df=imp_df,
        temporal_perf_df=temporal_perf_df,
        calibration_data=calibration_eval,
    )

    # Save summary report metadata
    summary_report = {
        "dataset_type": data_label,
        "is_synthetic": is_synthetic,
        "sample_counts": {"total": len(df_raw), "train": len(train_df), "val": len(val_df), "test": len(test_df)},
        "experiment1_baseline": exp1_results,
        "experiment2_imbalance": exp2_results,
        "experiment3_anomaly_fusion": exp3_results,
        "experiment4_graph_ablation": exp4_results,
        "gnn_gate_decision": gnn_gate_decision,
        "calibration": calibration_eval,
        "optimal_threshold": opt_threshold_info,
        "cost_analysis": {
            "cost_optimal_threshold": cost_analysis_res["cost_optimal_threshold"],
            "min_expected_loss": cost_analysis_res["min_expected_loss"],
        },
        "plot_files": plot_files,
    }

    with open(os.path.join(reports_dir, "experiment_summary.json"), "w") as f:
        json.dump(summary_report, f, indent=2)

    logger.info("Phase 3 Experiment Pipeline successfully executed end-to-end!")
    return summary_report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FinSight AI Phase 3 Experiment Runner")
    parser.add_argument("--synthetic", action="store_true", help="Force synthetic demonstration dataset mode")
    args = parser.parse_args()

    run_phase3_experiments(synthetic_override=args.synthetic)
