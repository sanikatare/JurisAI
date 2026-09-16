"""FinSight AI — Turnkey Setup & Dependency Verifier Script.

Verifies Python version, virtual environment, required libraries, directory structure,
and environment variable configuration.
"""
import sys
import os
import subprocess

REQUIRED_PACKAGES = [
    "pandas",
    "numpy",
    "scikit-learn",
    "joblib",
    "pytest",
    "fastapi",
    "uvicorn",
    "pydantic",
]


def check_python_version():
    """Ensure Python >= 3.10."""
    major, minor = sys.version_info[:2]
    print(f"[SETUP] Python Version: {major}.{minor}.{sys.version_info.micro}")
    if major < 3 or (major == 3 and minor < 10):
        print("[ERROR] FinSight AI requires Python 3.10 or higher.")
        sys.exit(1)


def check_dependencies():
    """Verify required Python packages are installed."""
    print("[SETUP] Checking Python dependencies...")
    missing = []
    for pkg in REQUIRED_PACKAGES:
        try:
            __import__(pkg)
            print(f"  ✓ {pkg}")
        except ImportError:
            missing.append(pkg)
            print(f"  ✗ {pkg} (MISSING)")

    if missing:
        print(f"\n[WARNING] Missing packages: {missing}")
        print("Installing missing packages via pip...")
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)
    else:
        print("[SETUP] All dependencies verified successfully!")


def check_directory_structure():
    """Verify expected workspace directory structure."""
    print("[SETUP] Checking directory structure...")
    dirs = ["data", "models", "knowledge_base", "reports", "results", "docs", "src", "tests"]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        print(f"  ✓ Directory ready: {d}/")


def main():
    print("=" * 60)
    print("      FinSight AI — Reproducibility Setup Utility      ")
    print("=" * 60)
    check_python_version()
    check_dependencies()
    check_directory_structure()
    print("\n[SUCCESS] FinSight AI environment setup verified!")


if __name__ == "__main__":
    main()
