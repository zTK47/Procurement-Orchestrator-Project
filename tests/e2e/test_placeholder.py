"""Placeholder so `pytest tests/e2e` collects at least one test and CI does
not silently report zero tests as success.

Real E2E tests (full FastAPI stack via httpx.AsyncClient / TestClient) are
tracked in docs/TASKS.md backlog, Phase 4 (Validate). They should exercise
the HTTP endpoints in interfaces/api/procurement_router.py end-to-end,
covering both intake modes (free text and direct catalog selection).
"""
import pytest


@pytest.mark.skip(reason="FastAPI E2E tests not yet implemented — see docs/TASKS.md backlog (Phase 4).")
def test_full_pipeline_via_http():
    ...
