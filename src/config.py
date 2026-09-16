"""Centralized Environment & Application Configuration — Phase 5 Part 3.

Loads and validates all environment variables and configuration settings.
Eliminates hardcoded values across backend, database, ML models, RAG, and GenAI services.
"""
from __future__ import annotations

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application Configuration Settings."""

    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development").lower()
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))

    # Security & API Auth
    API_KEY_SECRET: str = os.getenv("API_KEY_SECRET", "finsight-secret-key-change-in-production")
    REQUIRE_API_KEY: bool = os.getenv("REQUIRE_API_KEY", "false").lower() == "true"
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))

    # Database Connection
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "postgres")
    DB_NAME: str = os.getenv("DB_NAME", "finsight_db")
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    # ML Model & Registry
    MODEL_DIR: str = os.getenv("MODEL_DIR", "models")
    MODEL_VERSION: str = os.getenv("MODEL_VERSION", "v1.0.0")
    PRIMARY_MODEL_NAME: str = os.getenv("PRIMARY_MODEL_NAME", "Calibrated_Random_Forest")
    DEFAULT_RISK_THRESHOLD: float = float(os.getenv("DEFAULT_RISK_THRESHOLD", "0.2970"))

    # RAG & GenAI Settings
    KB_DIR: str = os.getenv("KB_DIR", "knowledge_base")
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "mock").lower()
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-4o-mini")
    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.1"))
    RAG_TOP_K: int = int(os.getenv("RAG_TOP_K", "5"))

    # MLOps & Monitoring
    DRIFT_THRESHOLD_WARNING: float = float(os.getenv("DRIFT_THRESHOLD_WARNING", "0.10"))
    DRIFT_THRESHOLD_ALERT: float = float(os.getenv("DRIFT_THRESHOLD_ALERT", "0.25"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()
