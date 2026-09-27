"""Placeholder so `pytest tests/integration` collects at least one test and
CI does not silently report zero tests as success.

Real integration tests (SQLAlchemy repositories against a running Postgres)
are tracked in docs/TASKS.md backlog, Phase 4 (Validate). They should mirror
the same scenarios already covered by the in-memory repository fakes in
tests/unit/, but assert against a real database round-trip.
"""
import pytest


@pytest.mark.skip(reason="SQLAlchemy repositories not yet implemented — see docs/TASKS.md backlog (Phase 4).")
def test_sqlalchemy_procurement_request_repository_round_trip():
    ...
