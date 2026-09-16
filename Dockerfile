# FinSight AI — Production Multi-Stage Dockerfile
FROM python:3.11-slim AS builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Final Production Stage
FROM python:3.11-slim AS runner

WORKDIR /app
ENV PYTHONUNBUFFERED=1 \
    PATH=/root/.local/bin:$PATH \
    ENVIRONMENT=production

COPY --from=builder /root/.local /root/.local

# Copy application source
COPY configs/ ./configs/
COPY rag/ ./rag/
COPY models/ ./models/
COPY database/ ./database/
COPY src/ ./src/
COPY docs/ ./docs/

# Create non-root system user for security
RUN useradd -m -u 1001 finsightuser && \
    chown -R finsightuser:finsightuser /app

USER finsightuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/v1/health')" || exit 1

CMD ["python", "-m", "uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
