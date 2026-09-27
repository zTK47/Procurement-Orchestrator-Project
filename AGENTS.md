# AGENTS.md

AI-Assisted Lean SDLC with Clean Architecture, TDD & CI/CD.

## WHY

Procurement Orchestrator turns a purchase need (free text or a catalog
selection) into a validated, approved purchase order, enforcing sourcing,
budget, and multi-level approval rules end-to-end. This is a university
capstone project (FHNW, BSc Business Information Technology, module
"AI-assisted Software Development"). Full context: `docs/PROJECT.md`.

## WHAT

- Python 3.12, FastAPI, SQLAlchemy 2.0, PostgreSQL (Neon), Pydantic v2.
- Clean Architecture, 4 layers: `domain/ -> application/ -> interfaces/ -> infrastructure/`.
- Dependency Rule: dependencies only point inward. `domain/` has zero
  third-party imports. Full architecture: `docs/PROJECT.md`.

## CURRENT PHASE

Load from `docs/TASKS.md` (source of truth for PHASE + STATUS).

## Workflow Phases

1. BOOTSTRAP: project scaffolding — see `skills/ai-sdlc-0-bootstrap/`.
2. SPECIFY: define acceptance criteria in `docs/specs/` — see `skills/ai-sdlc-1-specify/`.
3. DESIGN: architecture & test strategy, `docs/adr/` — see `skills/ai-sdlc-2-design/`.
4. DEVELOP: TDD implementation — see `skills/ai-sdlc-3-develop/`.
5. VALIDATE: full test pyramid + CI — see `skills/ai-sdlc-4-validate/`.
6. DEPLOY: containerized release — see `skills/ai-sdlc-5-deploy/`.

Each `skills/ai-sdlc-*/SKILL.md` is loaded on demand, only when the agent is
actually working in that phase (progressive disclosure — keeps this file
short and avoids wasting the instruction/context budget on irrelevant
phases).

## Fast Track

Small, localized regression fixes within existing behavior may skip the
full Specify/Design phases, but MUST start with a failing test. Fast Track
is NOT suitable for: new features, changes to the 5 core business rules
(see `docs/PROJECT.md`), new entities, or anything touching the approval
workflow state machine. Those always go through the full phase sequence.

## Non-negotiable rules

- `domain/` must never import from `application/`, `interfaces/`, or
  `infrastructure/`, and must never import third-party packages.
- No code without a failing test first (Red-Green-Refactor).
- Any LLM call must go through the `LLMAdapter` port (`application/ports/llm_adapter.py`);
  never call an LLM provider directly from `domain/` or `application/`.
- Architecture Decision Records (`docs/adr/`) start as `Proposed` and only
  become `Accepted` after an explicit team decision.

## Commands

```bash
# Run the full pipeline with zero dependencies installed
python demo.py

# Install dependencies
pip install -e ".[dev]"

# Tests
pytest tests/unit            # domain + application, no DB
pytest tests/integration     # requires a running Postgres (see docker-compose.yml)
pytest tests/e2e             # full FastAPI stack

# Lint
ruff check src tests

# Run the API locally
uvicorn procurement.infrastructure.main:app --reload

# Docker
docker build -t procurement-orchestrator .
docker compose up
```

## References

- Architecture, domain model, business rules: `docs/PROJECT.md`
- Live status: `docs/TASKS.md`
- Use case specs: `docs/specs/`
- Architecture decisions: `docs/adr/`
- Agent-usage notes for the presentation: `docs/LEARNINGS.md`
