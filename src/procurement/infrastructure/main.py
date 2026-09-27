"""FastAPI application entry point.

Repository/adapter wiring now happens via FastAPI's Depends mechanism (see
interfaces/api/dependencies.py) rather than app.state -- each request gets
its own DB session (infrastructure/db.py: get_db_session).

Run locally with:
    uvicorn procurement.infrastructure.main:app --reload
"""
from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from procurement.infrastructure.db import get_engine, get_session_factory
from procurement.infrastructure.models import Base
from procurement.infrastructure.seed_db import seed_database
from procurement.interfaces.api.procurement_router import router as procurement_router

STATIC_DIR = Path(__file__).parent.parent / "interfaces" / "static"


def create_app() -> FastAPI:
    app = FastAPI(
        title="Procurement Orchestrator",
        description="AI-assisted enterprise procurement request pipeline.",
        version="0.1.0",
    )

    @app.on_event("startup")
    def on_startup() -> None:
        engine = get_engine()
        Base.metadata.create_all(engine)
        session_factory = get_session_factory()
        session = session_factory()
        try:
            seed_database(session)
        finally:
            session.close()

    app.include_router(procurement_router)

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/")
    def frontend() -> FileResponse:
        return FileResponse(STATIC_DIR / "index.html")

    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

    return app


app = create_app()
