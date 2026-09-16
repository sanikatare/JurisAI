"""Database engine management. Credentials come ONLY from environment
variables (via .env) — never hardcoded here or anywhere else in src/."""
from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from src.utils.config import get_db_credentials


def get_engine() -> Engine:
    creds = get_db_credentials()
    url = (
        f"postgresql+psycopg2://{creds['DB_USER']}:{creds['DB_PASSWORD']}"
        f"@{creds['DB_HOST']}:{creds['DB_PORT']}/{creds['DB_NAME']}"
    )
    return create_engine(url, pool_pre_ping=True)
