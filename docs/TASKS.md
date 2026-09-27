# TASKS — Live Project Status

Source of truth for where the project stands. Update this whenever a phase
changes. STATUS is one of: `ready | in-progress | done | blocked`.
"done" means the phase's output has been verified, not just that code
exists (see AGENTS.md).

## Current

```
PHASE: 4-VALIDATE
STATUS: blocked
BLOCKER: SQLAlchemy/FastAPI layer written but NOT YET executed in any
         environment with network access + Postgres. Needs: `pip install
         -e ".[dev]"`, `docker compose up -d db`, then
         `pytest tests/unit tests/integration tests/e2e`. Report back any
         failures so they can be fixed.
```

## Done (verified — tests actually executed and passing)

- [x] Domain layer (entities, value objects, exceptions, 2 domain services) — 24 unit tests
- [x] Application layer (6 use cases + abstract ports) — 20 unit tests
- [x] **44/44 unit tests passing**, zero DB/FastAPI/SQLAlchemy dependency
- [x] `demo.py` — full pipeline (both intake modes), runs with zero installed dependencies, verified
- [x] AGENTS.md + 6 SKILL.md files
- [x] docs/specs/ (6 use case specs, Given/When/Then)
- [x] docs/adr/ (5 ADRs; **ADR-002 still Proposed**, pending team decision)

## Done (written, syntax-checked with py_compile, NOT yet executed)

These were built in a sandboxed environment with no network access, so
FastAPI/SQLAlchemy/pytest could not actually be installed/run here. They
must be verified in your own environment as the very next step:

- [ ] SQLAlchemy repositories (`infrastructure/repositories/sqlalchemy_*.py`)
      for all 6 ports — mapping ORM models <-> domain entities
- [ ] FastAPI dependency wiring via `Depends` (`interfaces/api/dependencies.py`)
      replacing the earlier app.state-based wiring
- [ ] `infrastructure/main.py` — creates tables + seeds DB on startup, serves
      the frontend, mounts the router
- [ ] `infrastructure/seed_db.py` — idempotent DB seeding from the same
      demo data used by demo.py
- [ ] Minimal frontend (`interfaces/static/index.html`) — vanilla JS calling
      every endpoint, served at `/`
- [ ] `tests/integration/` — 4 files, real repository round-trip tests
      against Postgres, isolated via SAVEPOINT-rollback (`tests/conftest.py`)
- [ ] `tests/e2e/` — 2 files, full HTTP pipeline via FastAPI's `TestClient`,
      with dependency_overrides reusing the isolated test session

## Backlog

- [ ] **Run the above and fix whatever breaks** (highest priority)
- [ ] Confirm/reject ADR-002 (price-tie handling) as a team — currently `Proposed`
- [ ] Deploy to Render + Neon (Phase 5), manual end-to-end verification
      against the live URL (not just green CI)
- [ ] `docs/LEARNINGS.md` — coding-agent usage notes for the presentation
      (fill in as you go, not at the end)
- [ ] Push to GitHub: `git remote add origin <repo-url> && git push -u origin master`
  (no GitHub connector was available to push directly from this session)

## Notes

- Repository/adapter selection is via `interfaces/api/dependencies.py`
  (`get_llm_adapter`, `get_*_repository`) — this is the single place to
  change if you swap the LLM provider or persistence technology later.
- `demo.py` deliberately still uses the in-memory repositories (zero
  dependencies) — it is a sanity-check tool, not the production wiring.
