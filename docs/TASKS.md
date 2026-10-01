# TASKS

## Current

PHASE: 3
STATUS: in-progress
UC: UC-007 … UC-009 (ERP hand-off) implemented; integration and e2e tests not yet run
BLOCKER: none, but the SQLAlchemy layer and both test suites have never been executed
(no network access where they were written). First action: run the commands below and fix.

```bash
pip install -e ".[dev]" && docker compose up -d db
pytest tests/unit tests/integration tests/e2e
```

## Backlog

- [ ] Run integration + e2e tests, fix failures (then PHASE 3 → done, PHASE 4 → ready)
- [ ] Team decision on ADR-001 … ADR-006 (all Proposed): accept, change or reject, with review reference
- [ ] From now on write each test first and commit red → green (the scaffold was generated tests-and-code together)
- [ ] Trim comments/docstrings to the "avoid unnecessary comments" rule
- [ ] Compare with the professor's template files not readable here: `skills/*/SKILL.md`, `docs/specs/UC-TEMPLATE.md`, `.devcontainer`
- [ ] VALIDATE: coverage check, release workflow tag `v0.1.0`
- [ ] DEPLOY: Render + Neon, then record the live smoke-test result here
- [ ] Optional: real LLM adapter (LiteLLM), configurable price-tie strategy, `ApprovalWorkflow` entity

## Order PDF Orchestration (OPO) — second bounded context

PHASE: 3
STATUS: in-progress
UC: OPO-UC-001 … OPO-UC-006 (specs written first, 2026-10-01)

- [x] SPECIFY: `docs/specs/OPO-UC-001` … `OPO-UC-006`
- [x] DESIGN: section in `docs/PROJECT.md`; ADR-007, ADR-008 (Proposed)
- [ ] DEVELOP: one red → green commit pair per rule and use case
- [ ] Team decision on ADR-007 and ADR-008
- [ ] Later: real agent via the FHNW LiteLLM gateway (key from env), document upload (PDF/DOCX), persistence, Dockerfile entry for the second app

## Validation evidence

| Date | Command | Result |
|---|---|---|
| 2026-09-28 | `tests/unit via a stdlib pytest shim (pytest could not be installed)` | 64 passed |
| 2026-09-28 | `python demo.py` | pipeline reaches COMPLETED |
| — | `pytest tests/integration tests/e2e` | not run yet |

## Decisions

See `docs/adr/`. No decision is Accepted yet.
