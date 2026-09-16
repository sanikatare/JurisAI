"""FinSight AI — Production Application & Service Stack Launcher.

Launches the production FastAPI server using Uvicorn with environment validation.
"""
import sys
import os
import uvicorn

from src.utils.logger import get_logger

logger = get_logger("script_deploy")


def main():
    print("=" * 60)
    print("      FinSight AI — Production Stack Launcher            ")
    print("=" * 60)

    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))

    print(f"[DEPLOY] Starting FastAPI application on http://{host}:{port}...")
    print(f"[DEPLOY] Interactive Swagger Docs available at http://{host}:{port}/docs")
    print(f"[DEPLOY] Health check endpoint: http://{host}:{port}/api/v1/health")

    uvicorn.run("src.api.app:app", host=host, port=port, reload=False, log_level="info")


if __name__ == "__main__":
    main()
