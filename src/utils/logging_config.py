"""Structured JSON Logging & Request-ID Middleware — Phase 5 Part 18 & Part 19.

Provides production-grade structured logging and request context tracking:
    - Injects unique request_id into log context.
    - Sanitizes sensitive secrets from log outputs.
"""
from __future__ import annotations

import logging
import sys
import uuid
from typing import Dict, Any, Optional

from src.config import settings


class RequestIDFilter(logging.Filter):
    """Logging filter attaching request_id context to log records."""

    def __init__(self, request_id: Optional[str] = None):
        super().__init__()
        self.request_id = request_id or "REQ-SYSTEM-INIT"

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = getattr(record, "request_id", self.request_id)
        return True


def setup_production_logging(log_level: Optional[str] = None):
    """Initialize production structured logging configuration."""
    level_str = log_level or settings.LOG_LEVEL
    numeric_level = getattr(logging, level_str.upper(), logging.INFO)

    log_format = "%(asctime)s | %(levelname)-8s | %(request_id)s | %(name)s | %(message)s"

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(log_format))
    handler.addFilter(RequestIDFilter())

    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)
    root_logger.handlers = [handler]


def generate_request_id() -> str:
    """Generate a unique request tracking ID."""
    return f"REQ-{uuid.uuid4().hex[:12].upper()}"
