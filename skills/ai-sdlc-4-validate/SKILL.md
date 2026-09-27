---
name: ai-sdlc-4-validate
description: Run the full testing pyramid and CI checks before considering a phase done.
---

# PHASE 4 — VALIDATE

## Testing Pyramid
1. `pytest tests/unit` — domain + application, mocked/in-memory repos, no
   DB, must run in under a few seconds.
2. `pytest tests/integration` — concrete SQLAlchemy repositories against a
   real Postgres (docker-compose or Neon), verifies persistence mapping.
3. `pytest tests/e2e` — full FastAPI app via `httpx`, verifies the whole
   pipeline through HTTP.

## CI Pipeline (`.github/workflows/ci.yml`)
lint (ruff) -> unit tests -> integration tests (Postgres service container)
-> docker build.

## Rules
- "Done" means the phase's output was actually verified, not just that
  code exists. A green CI run on an empty test file is not evidence of
  anything.
- Update `docs/TASKS.md`: `PHASE: 4-VALIDATE`, `STATUS: done` only once all
  three test levels pass in CI.
