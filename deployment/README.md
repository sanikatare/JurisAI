# FinSight AI — Deployment & CI/CD Configurations

## Overview
This directory contains production deployment manifests, containerization configurations, and CI/CD automated test workflows.

---

## Directory Structure
```
deployment/
├── docker/
│   ├── Dockerfile            # Multi-stage production container build
│   └── docker-compose.yml    # Multi-service stack (PostgreSQL, Backend API, Web UI)
├── github-actions/
│   └── ci.yml                # GitHub Actions automated test & build pipeline
└── README.md
```

## Production Launch Command
```powershell
docker-compose up -d
```
