---
name: ai-sdlc-4-validate
description: Collect evidence that the use case is release-ready.
---

# 4 VALIDATE — What evidence supports readiness?

1. `pytest tests/unit`, `pytest tests/integration` (Postgres via `docker compose up -d db`), `pytest tests/e2e`.
2. `ruff check src tests`; `docker build -t procurement-orchestrator .` and run the container.
3. GitHub Actions `ci.yml` green on the pull request; coverage as a heuristic (about 80%), not proof.
4. Record commit, commands and real results in `docs/TASKS.md`; note known limitations.

A failed gate goes back to DEVELOP or SPECIFY; it is never bypassed. A green structural check is not application evidence. Record `PHASE: 4`.
