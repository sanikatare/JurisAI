"""Tests for ModelRegistry and versioning — Phase 5."""
import pytest
import os

from src.ml.registry import ModelRegistry


def test_model_registry_initialization():
    """Verify ModelRegistry loads v1 production model artifacts and metadata."""
    registry = ModelRegistry(root_dir="models")
    models = registry.list_models()

    assert len(models) > 0
    assert models[0]["version"] == "v1.0.0"

    model, prep, calib, meta = registry.get_production_model()
    assert meta["status"] == "production"
