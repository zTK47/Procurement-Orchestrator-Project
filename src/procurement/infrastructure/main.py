"""FastAPI application entry point.

This module is the ONLY place where concrete infrastructure classes
(in-memory repositories today, SQLAlchemy ones from Phase 4 onward) are
instantiated and injected into the application layer. Everything upstream
(use cases, domain) only ever sees abstractions.

Run locally with:
    uvicorn procurement.infrastructure.main:app --reload
"""
from __future__ import annotations

from fastapi import FastAPI

from procurement.infrastructure.in_memory_repositories import (
    InMemoryApprovalRepository,
    InMemoryCatalogItemRepository,
    InMemoryCostCenterRepository,
    InMemoryProcurementRequestRepository,
    InMemorySupplierRepository,
    InMemoryUserRepository,
)
from procurement.infrastructure.mock_llm_adapter import MockLLMAdapter
from procurement.infrastructure.seed_data import build_seed_data
from procurement.interfaces.api.procurement_router import router as procurement_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Procurement Orchestrator",
        description="AI-assisted enterprise procurement request pipeline.",
        version="0.1.0",
    )

    suppliers, catalog_items, cost_centers, users = build_seed_data()

    # Dependency Injection: concrete adapters/repositories wired here only.
    app.state.llm_adapter = MockLLMAdapter()
    app.state.procurement_repository = InMemoryProcurementRequestRepository()
    app.state.catalog_repository = InMemoryCatalogItemRepository(catalog_items)
    app.state.supplier_repository = InMemorySupplierRepository(suppliers)
    app.state.cost_center_repository = InMemoryCostCenterRepository(cost_centers)
    app.state.user_repository = InMemoryUserRepository(users)
    app.state.approval_repository = InMemoryApprovalRepository()

    app.include_router(procurement_router)

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
