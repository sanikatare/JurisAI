"""Central logging setup so every pipeline stage logs consistently."""
from __future__ import annotations

import logging
import sys
from pathlib import Path


def get_logger(name: str, log_dir: str | Path = "reports/logs", level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger  # avoid duplicate handlers on repeated calls

    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(fmt)
    logger.addHandler(console)

    try:
        log_path = Path(log_dir)
        log_path.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_path / f"{name}.log")
        file_handler.setFormatter(fmt)
        logger.addHandler(file_handler)
    except OSError:
        # If the filesystem is read-only or path invalid, fall back to console-only.
        logger.warning("Could not create file handler for logs; continuing with console only.")

    return logger
