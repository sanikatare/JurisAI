# Production Deployment Guide — FinSight AI

## 1. Prerequisites
- Docker Engine 20.10+ & Docker Compose 2.0+
- Python 3.11+
- PostgreSQL 15+ (if running outside Docker)

---

## 2. Dockerized Local & Cloud Deployment

```bash
# 1. Clone repository & configure secrets
git clone https://github.com/organization/FinSight-AI.git
cd FinSight-AI
cp .env.example .env

# 2. Build and launch multi-container stack via Docker Compose
docker-compose up --build -d

# 3. Verify health status
curl http://localhost:8000/api/v1/health
curl http://localhost:8000/api/v1/ready
```

---

## 3. Production Environment Variables Reference

| Variable Name | Default Value | Description |
|---|---|---|
| `ENVIRONMENT` | `production` | Execution environment mode |
| `DATABASE_URL` | `postgresql://postgres:postgrespassword@postgres:5432/finsight_db` | PostgreSQL connection URI |
| `MODEL_VERSION` | `v1.0.0` | Active model version in `models/v1/` |
| `LLM_PROVIDER` | `mock` | LLM Provider (`openai`, `gemini`, `mock`) |
| `API_PORT` | `8000` | FastAPI server port |

---

## 4. Troubleshooting & Operational Health Checks
- **Health Endpoint**: `GET /api/v1/health` $\to$ Returns HTTP 200 OK.
- **Readiness Endpoint**: `GET /api/v1/ready` $\to$ Verifies database, model, and RAG vector store readiness.
