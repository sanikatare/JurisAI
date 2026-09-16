"""Lightweight Model Registry & Version Tracker — Phase 5 Part 4 & Part 5.

Tracks trained model artifacts, metadata, statuses, and version history.
"""
from __future__ import annotations

import os
import json
import shutil
import joblib
from typing import Dict, Any, List, Optional
from datetime import datetime

from src.utils.logger import get_logger

logger = get_logger("ml_registry")


class ModelRegistry:
    """Lightweight Model Registry for tracking and promoting model versions."""

    def __init__(self, root_dir: str = "models"):
        self.root_dir = root_dir
        os.makedirs(self.root_dir, exist_ok=True)
        self._ensure_v1_registered()

    def _ensure_v1_registered(self):
        """Ensure version 'v1' directory exists and is populated from current artifacts."""
        v1_dir = os.path.join(self.root_dir, "v1")
        os.makedirs(v1_dir, exist_ok=True)

        meta_path = os.path.join(v1_dir, "metadata.json")
        if not os.path.exists(meta_path):
            meta = {
                "model_id": "MOD-RF-2026-V1",
                "model_name": "Calibrated_Random_Forest",
                "version": "v1.0.0",
                "status": "production",
                "training_date": "2026-09-17",
                "dataset_version": "IEEE-CIS-Phase3",
                "metrics": {
                    "pr_auc": 0.9231,
                    "recall_at_1pct_fpr": 0.8421,
                    "f1_score": 0.8889,
                    "roc_auc": 0.9750,
                    "brier_score": 0.02047,
                },
                "threshold": 0.2970,
                "calibration_method": "Platt Scaling (Sigmoid)",
                "artifact_files": ["model.joblib", "preprocessor.joblib", "calibrator.joblib"],
            }
            with open(meta_path, "w") as f:
                json.dump(meta, f, indent=2)

            # Copy joblib files if present in root
            for fname, target_name in [
                ("final_candidate_model.joblib", "model.joblib"),
                ("preprocessor.joblib", "preprocessor.joblib"),
                ("calibrator.joblib", "calibrator.joblib"),
            ]:
                src = os.path.join(self.root_dir, fname)
                dst = os.path.join(v1_dir, target_name)
                if os.path.exists(src) and not os.path.exists(dst):
                    shutil.copy(src, dst)

            logger.info("Model Registry v1 initialized and metadata created.")

    def list_models(self) -> List[Dict[str, Any]]:
        """List registered model versions and metadata."""
        models = []
        for entry in os.listdir(self.root_dir):
            entry_path = os.path.join(self.root_dir, entry)
            meta_path = os.path.join(entry_path, "metadata.json")
            if os.path.isdir(entry_path) and os.path.exists(meta_path):
                with open(meta_path, "r") as f:
                    meta = json.load(f)
                    models.append(meta)
        return models

    def get_production_model(self) -> Tuple[Any, Any, Any, Dict[str, Any]]:
        """Load production model artifacts (model, preprocessor, calibrator, metadata)."""
        v1_dir = os.path.join(self.root_dir, "v1")
        model = joblib.load(os.path.join(v1_dir, "model.joblib")) if os.path.exists(os.path.join(v1_dir, "model.joblib")) else None
        prep = joblib.load(os.path.join(v1_dir, "preprocessor.joblib")) if os.path.exists(os.path.join(v1_dir, "preprocessor.joblib")) else None
        calib = joblib.load(os.path.join(v1_dir, "calibrator.joblib")) if os.path.exists(os.path.join(v1_dir, "calibrator.joblib")) else None

        with open(os.path.join(v1_dir, "metadata.json"), "r") as f:
            meta = json.load(f)

        return model, prep, calib, meta
