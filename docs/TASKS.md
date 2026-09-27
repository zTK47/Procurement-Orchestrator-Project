# TASKS — Live Project Status

Source of truth for where the project stands. Update this whenever a phase
changes. STATUS is one of: `ready | in-progress | done | blocked`.
"done" means the phase's output has been verified, not just that code
exists (see AGENTS.md).

## Current

```
PHASE: 3-DEVELOP
USE_CASE: (all 6 core use cases implemented; interfaces/infrastructure wiring in progress)
STATUS: in-progress
```

## Done

- [x] UC-001 ParseRequestUseCase — domain + application, 2 unit tests, done 24.09.2026
- [x] UC-002 ResolveItemUseCase — domain (SourcingRule, 7 unit tests) + application (1 unit test), done 24.09.2026
- [x] UC-003 ValidateRequestUseCase — 2 unit tests, done 24.09.2026
- [x] UC-004 CreateOrderUseCase — 3 unit tests, done 24.09.2026
- [x] UC-005 SubmitCatalogSelectionUseCase — 4 unit tests, done 24.09.2026
- [x] UC-006 RecordApprovalDecisionUseCase — 7 unit tests, done 24.09.2026
- [x] ProcurementRequest state machine — 8 unit tests, done 24.09.2026
- [x] Money value object invariants — 5 unit tests, done 24.09.2026
- [x] AGENTS.md + 6 SKILL.md files — done 24.09.2026
- [x] docs/specs/ (6 use case specs, Given/When/Then) — done 24.09.2026
- [x] docs/adr/ (5 ADRs; ADR-002 still Proposed, pending team decision)
- [x] demo.py — full pipeline runnable with zero external dependencies, verified
- [x] 44/44 unit tests passing (domain + application layers)

## Backlog

- [ ] Confirm/reject ADR-002 (price-tie handling) as a team — currently `Proposed`
- [ ] `tests/integration/` — SQLAlchemy repositories against real Postgres (Phase 4)
- [ ] `tests/e2e/` — full FastAPI stack via httpx (Phase 4)
- [ ] Wire SQLAlchemy repositories into `infrastructure/main.py`, replacing in-memory ones
- [ ] `.github/workflows/ci.yml` — lint → unit → integration → docker build
- [ ] `Dockerfile` + `docker-compose.yml` (local Postgres)
- [ ] Deploy to Render + Neon (Phase 5), manual end-to-end verification
- [ ] Minimal frontend (HTML/Jinja2/HTMX or static JS) calling the API
- [ ] `docs/LEARNINGS.md` — coding-agent usage notes for the presentation
- [ ] README.md (final, polished, for submission)

## Notes

- Team split: see README.md "Team & course context" once written.
- ADR-002 is the one open design decision requiring an explicit team call
  before submission (see AGENTS.md "Architecture Gates").
