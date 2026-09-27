# TASKS — Live Project Status

Source of truth for where the project stands. Update this whenever a phase
changes. STATUS is one of: `ready | in-progress | done | blocked`.
"done" means the phase's output has been verified, not just that code
exists (see AGENTS.md).

## Current

```
PHASE: 4-VALIDATE
STATUS: blocked
BLOCKER: The full stack (SQLAlchemy + FastAPI + integration/e2e tests) has
         been written and manually code-reviewed (3 real bugs found and
         fixed during review -- see "Bugs found during review" below), but
         has NEVER been executed: the development sandbox used to build it
         has no network access to install FastAPI/SQLAlchemy/pytest.
NEXT STEP (do this first): in an environment with network access —
  1. pip install -e ".[dev]"
  2. docker compose up -d db
  3. pytest tests/unit tests/integration tests/e2e
  4. Fix whatever fails (some issues are likely, despite the review pass —
     manual review catches obvious bugs, not everything a real run would)
```

## Done (verified — tests actually executed and passing)

- [x] Domain layer (entities, value objects, exceptions, 2 domain services) — 24 unit tests
- [x] Application layer (6 use cases + abstract ports) — 20 unit tests
- [x] **44/44 unit tests passing**, zero DB/FastAPI/SQLAlchemy dependency
- [x] `demo.py` — full pipeline (both intake modes), runs with zero installed dependencies, verified
- [x] AGENTS.md + 6 SKILL.md files
- [x] docs/specs/ (6 use case specs, Given/When/Then)
- [x] docs/adr/ (5 ADRs, all **Accepted**)
- [x] docs/LEARNINGS.md — populated with concrete examples from this project's own bootstrap process

## Done (written, code-reviewed, NOT yet executed)

Built in a sandboxed environment with no network access, so
FastAPI/SQLAlchemy/pytest could not be installed/run there. A manual code
review pass was done instead of execution, and found + fixed 3 real bugs
(listed below) — but review is not a substitute for actually running the
tests. Do that first, before anything else:

- [ ] SQLAlchemy repositories (`infrastructure/repositories/sqlalchemy_*.py`)
- [ ] FastAPI dependency wiring via `Depends` (`interfaces/api/dependencies.py`)
- [ ] `infrastructure/main.py` — lifespan-based startup (creates tables,
      seeds DB), serves the frontend, mounts the router
- [ ] `infrastructure/seed_db.py` — idempotent DB seeding
- [ ] Minimal frontend (`interfaces/static/index.html`)
- [ ] `tests/integration/` — 4 files, real repository round-trip tests
- [ ] `tests/e2e/` — 2 files, full HTTP pipeline via `TestClient`

### Bugs found during manual review (already fixed in this codebase)

1. `parsed_confidence` read back from a `Numeric` column as a `Decimal` by
   the psycopg2 driver, but passed directly into `ParsedRequest(confidence=...)`
   which is typed `float` — fixed with an explicit `float(...)` cast in
   `sqlalchemy_procurement_request_repository.py`.
2. Integration tests for the `Approval` repository created `Approval`
   objects referencing `procurement_request_id`/`approver_id` values with
   **no matching parent rows** — would have failed with a foreign-key
   constraint violation on the very first real test run. Fixed by adding a
   `_seed_parent_rows` helper in `tests/integration/test_approval_repository.py`.
3. `main.py` used the deprecated `@app.on_event("startup")` API — modernized
   to a `lifespan` context manager (current FastAPI best practice).

**This is not an exhaustive list** — these are only the bugs visible
through static reading of the code. Runtime-only issues (typos in column
names vs. actual Postgres behavior, session lifecycle edge cases, Pydantic
v2 serialization quirks, etc.) can only be caught by actually running
`pytest`.

## Backlog

- [ ] **Run the full test suite and fix whatever breaks** (highest priority)
- [ ] Deploy to Render + Neon (Phase 5), manual end-to-end verification
      against the live URL (not just green CI)
- [ ] Continue filling `docs/LEARNINGS.md` with your own coding-agent
      session notes as you work through any remaining fixes
- [ ] Push to GitHub: `git remote add origin <repo-url> && git push -u origin master`

## Notes

- Repository/adapter selection is centralized in `interfaces/api/dependencies.py`.
- `demo.py` deliberately still uses the in-memory repositories (zero
  dependencies) — a sanity-check tool, not the production wiring.
- Git history in this repo currently has commits made in a single bootstrap
  session (this is a starting scaffold, not a record of organic
  incremental work) — your own commits from here on, made as you actually
  fix issues and progress through phases, are what will show real
  AI-SDLC process discipline to the grader.
