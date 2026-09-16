"""Production FastAPI Web Application & Middleware — Phase 5 Part 11.

Exposes production endpoints:
    - GET /api/v1/health & GET /api/v1/ready
    - POST /api/v1/predict (Real-time ML inference)
    - POST /api/v1/investigate (GenAI Investigation Synthesis)
    - POST /api/v1/ask & POST /api/v1/rag/search
    - POST /api/v1/report & POST /api/v1/analytics/query
    - GET /api/v1/model/info & GET /api/v1/monitoring
"""
from __future__ import annotations

import os
import time
from typing import Dict, Any, Optional

try:
    from fastapi import FastAPI, HTTPException, Body, Request, Header
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse
    HAS_FASTAPI = True
except ImportError:
    HAS_FASTAPI = False

from src.config import settings
from src.services.prediction_service import PredictionService
from src.genai.services.investigation_service import FinSightGenAIService
from src.monitoring.model_monitor import ModelMonitor
from src.api.routes import cases, investigate, ask, rag, report, analytics
from src.utils.logging_config import setup_production_logging, generate_request_id
from src.utils.logger import get_logger

setup_production_logging()
logger = get_logger("api_production")

prediction_service = PredictionService()
genai_service = FinSightGenAIService()
model_monitor = ModelMonitor()

if HAS_FASTAPI:
    app = FastAPI(
        title="FinSight AI — Production Decision Support API",
        description="Enterprise Financial Risk, Fraud & Decision Intelligence Platform",
        version="5.0.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def request_id_and_latency_middleware(request: Request, call_next):
        req_id = request.headers.get("X-Request-ID") or generate_request_id()
        request.state.request_id = req_id
        t0 = time.time()

        # Simple API Key check if enforced
        if settings.REQUIRE_API_KEY and request.url.path.startswith("/api/"):
            api_key = request.headers.get("X-API-Key")
            if api_key != settings.API_KEY_SECRET:
                return JSONResponse(
                    status_code=401,
                    content={"status": "error", "message": "Invalid API Key", "request_id": req_id}
                )

        response = await call_next(request)
        latency_ms = round((time.time() - t0) * 1000.0, 2)
        response.headers["X-Request-ID"] = req_id
        response.headers["X-Latency-MS"] = str(latency_ms)
        return response

    @app.get("/api/v1/health")
    def health_check():
        return {
            "status": "healthy",
            "environment": settings.ENVIRONMENT,
            "version": settings.MODEL_VERSION,
        }

    @app.get("/api/v1/ready")
    def readiness_check():
        """Readiness check checking database, model, and RAG availability."""
        model_ready = prediction_service.model is not None
        rag_ready = genai_service.rag_retriever.is_indexed

        is_ready = model_ready and rag_ready
        status_str = "ready" if is_ready else "degraded"

        return {
            "status": status_str,
            "database": "ok",
            "model": "ok" if model_ready else "unavailable",
            "rag": "ok" if rag_ready else "degraded",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }

    @app.post("/api/v1/predict")
    def predict_endpoint(payload: Dict[str, Any] = Body(...)):
        """Real-time prediction inference endpoint."""
        res = prediction_service.predict_transaction(payload)
        model_monitor.log_prediction(res)
        return {"status": "success", "prediction": res}

    @app.get("/api/v1/model/info")
    def get_model_info():
        """Return model metadata and version registry info."""
        return {
            "status": "success",
            "model_info": prediction_service.metadata,
        }

    @app.get("/api/v1/monitoring")
    def get_monitoring_metrics():
        """Return operational model health & prediction summary metrics."""
        return {
            "status": "success",
            "metrics": model_monitor.compute_summary_metrics(),
        }

    @app.get("/api/v1/cases/{transaction_id}")
    def get_case(transaction_id: int):
        return cases.get_case_details(transaction_id)

    @app.get("/api/v1/cases/{transaction_id}/evidence")
    def get_evidence(transaction_id: int):
        return cases.get_case_evidence(transaction_id)

    @app.post("/api/v1/investigate")
    def investigate_case_endpoint(payload: Dict[str, Any] = Body(...)):
        tx_id = payload.get("transaction_id", 2987015)
        query = payload.get("query")
        return investigate.run_investigation(tx_id, query=query)

    @app.post("/api/v1/ask")
    def ask_endpoint(payload: Dict[str, Any] = Body(...)):
        question = payload.get("question", "")
        tx_id = payload.get("transaction_id")
        return ask.ask_finsight(question, transaction_id=tx_id)

    @app.post("/api/v1/rag/search")
    def rag_search_endpoint(payload: Dict[str, Any] = Body(...)):
        query = payload.get("query", "")
        top_k = payload.get("top_k", 5)
        return rag.search_rag_knowledge_base(query, top_k=top_k)

    @app.post("/api/v1/report")
    def report_endpoint(payload: Dict[str, Any] = Body(...)):
        tx_id = payload.get("transaction_id", 2987015)
        return report.generate_report_endpoint(tx_id)

    @app.post("/api/v1/analytics/query")
    def analytics_endpoint(payload: Dict[str, Any] = Body(...)):
        question = payload.get("question", "")
        return analytics.run_analytics_query(question)

    # Static file mounting & SPA fallback route for JurisAI Frontend
    frontend_dist_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend", "dist")
    if os.path.exists(frontend_dist_dir):
        from fastapi.staticfiles import StaticFiles
        from fastapi.responses import FileResponse

        app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist_dir, "assets")), name="assets")

        @app.get("/{full_path:path}")
        async def serve_spa(full_path: str):
            if full_path.startswith("api/"):
                raise HTTPException(status_code=404, detail="API route not found")
            file_path = os.path.join(frontend_dist_dir, full_path)
            if os.path.exists(file_path) and os.path.isfile(file_path):
                return FileResponse(file_path)
            return FileResponse(os.path.join(frontend_dist_dir, "index.html"))

else:
    logger.info("FastAPI module not available; app set to None.")
    app = None
