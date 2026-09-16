# Slide 12: MLOps, Containerization & Drift Monitoring

## Production Engineering & Governance
- **FastAPI REST Service**: Rate-limited, authenticated API exposing `/predict`, `/investigate`, `/monitoring`, `/health`.
- **Model Registry**: Immutable artifact store managing candidate `v1.0.0` metadata.
- **Population Stability Index (PSI)**: Monitors real-time feature distribution drift, categorizing features into `NORMAL`, `WARNING`, and `DRIFT`.
- **Dockerization**: Multi-stage `Dockerfile` and `docker-compose.yml` orchestrating PostgreSQL, API backend, and UI.
