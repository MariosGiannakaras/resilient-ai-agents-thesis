"""FastAPI application shell for the local thesis UI.

This module intentionally exposes only truthful, read-only application data at
this scaffold stage. Active-run supervision/WebSocket streaming belongs to
T-530 and must not be simulated here.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from resilient_agents.experiment_manager import ExperimentRegistry, get_resource_snapshot

API_SCHEMA_VERSION = 1
REPO_ROOT = Path(__file__).resolve().parents[2]
FRONTEND_DIST = REPO_ROOT / "frontend" / "dist"

app = FastAPI(
    title="Resilient AI Agents Thesis Application",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url=None,
    openapi_url="/api/openapi.json",
)

# Development-only Vite origins. The supported thesis-user path is same-origin
# FastAPI serving the prebuilt SPA, so CORS is unnecessary in normal use.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


def _registry() -> ExperimentRegistry:
    return ExperimentRegistry(REPO_ROOT)


@app.get("/api/health")
def health() -> dict[str, Any]:
    """Return application-shell status without claiming runtime readiness."""
    return {
        "api_schema_version": API_SCHEMA_VERSION,
        "status": "ok",
        "frontend_built": (FRONTEND_DIST / "index.html").is_file(),
        "active_runtime_service": "not-yet-implemented",
    }


@app.get("/api/system")
def system_snapshot() -> dict[str, Any]:
    """Return the canonical real resource snapshot or explicit unavailable state."""
    return get_resource_snapshot(REPO_ROOT)


@app.get("/api/runs")
def list_finalized_runs() -> dict[str, Any]:
    """Return integrity-validated finalized-run history only.

    Unfinished/active runs are intentionally not inferred from this registry;
    T-530 will expose them through a dedicated runtime service.
    """
    try:
        runs = _registry().list_runs()
    except (OSError, ValueError) as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return {"api_schema_version": API_SCHEMA_VERSION, "runs": runs}


@app.get("/api/runs/{run_id}")
def get_finalized_run(run_id: str) -> dict[str, Any]:
    try:
        run = _registry().get_run(run_id)
    except (OSError, ValueError) as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    if run is None:
        raise HTTPException(status_code=404, detail="run not found")
    return {"api_schema_version": API_SCHEMA_VERSION, "run": run}


if (FRONTEND_DIST / "assets").is_dir():
    app.mount(
        "/assets",
        StaticFiles(directory=FRONTEND_DIST / "assets"),
        name="frontend-assets",
    )


@app.get("/{frontend_path:path}", include_in_schema=False)
def serve_frontend(frontend_path: str) -> FileResponse | JSONResponse:
    """Serve the prebuilt Vite SPA and preserve client-side routing.

    API paths are declared above and therefore resolved before this catch-all.
    Missing build output is an explicit service-unavailable state, never a
    generated placeholder pretending that the UI is ready.
    """
    index_path = FRONTEND_DIST / "index.html"
    if not index_path.is_file():
        return JSONResponse(
            status_code=503,
            content={
                "status": "frontend-unavailable",
                "detail": "frontend/dist is missing; build the validated frontend",
            },
        )

    requested = (FRONTEND_DIST / frontend_path).resolve()
    try:
        requested.relative_to(FRONTEND_DIST.resolve())
    except ValueError:
        requested = index_path
    if frontend_path and requested.is_file():
        return FileResponse(requested)
    return FileResponse(index_path)
