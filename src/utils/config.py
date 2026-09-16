"""Config loading utility.

Loads configs/config.yaml plus .env, so nothing in the rest of src/ ever
hardcodes a path or a credential. This is the single place that knows
where the project root is.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def load_config(config_path: str | Path = "configs/config.yaml") -> dict[str, Any]:
    """Load the YAML config, resolving relative paths against the project root."""
    load_dotenv(PROJECT_ROOT / ".env", override=False)

    full_path = Path(config_path)
    if not full_path.is_absolute():
        full_path = PROJECT_ROOT / full_path

    if not full_path.exists():
        raise FileNotFoundError(
            f"Config file not found at {full_path}. "
            "Did you run this from the project root?"
        )

    with open(full_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    # Resolve path entries to absolute paths against project root.
    for key, value in config.get("paths", {}).items():
        config["paths"][key] = str(PROJECT_ROOT / value)

    return config


def get_db_credentials() -> dict[str, str]:
    """Read DB credentials from environment variables only — never from source."""
    required = ["DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD"]
    missing = [v for v in required if os.environ.get(v) is None]
    if missing:
        raise EnvironmentError(
            f"Missing required environment variables: {missing}. "
            "Copy .env.example to .env and fill in real values."
        )
    return {v: os.environ[v] for v in required}
