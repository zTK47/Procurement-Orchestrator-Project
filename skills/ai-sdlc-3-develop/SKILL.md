---
name: ai-sdlc-3-develop
description: Implement the current use case using strict Red-Green-Refactor TDD.
---

# PHASE 3 — DEVELOP

## Order
1. Domain unit tests -> domain implementation (entities, value objects,
   domain services). No third-party imports allowed here.
2. Application unit tests (using `InMemory*` fakes for repositories/adapters)
   -> use case implementation.
3. Only once 1-2 are green: interfaces (Pydantic schemas, FastAPI router)
   and infrastructure (repository/adapter implementations) wiring.

## TDD Loop
RED -> GREEN -> REFACTOR, one acceptance criterion at a time:
1. Write ONE failing test matching one Given/When/Then from the spec.
2. Write the minimal code to make it pass. Do not add behavior the test
   does not require.
3. Refactor (naming, duplication) with the test suite green throughout.
4. Repeat for the next criterion.

## Rules
- Tests before code, always.
- Respect the Dependency Rule (see docs/PROJECT.md).
- If a requirement is unclear or contradicts an existing ADR/spec, stop and
  ask rather than guessing.
- Update `docs/TASKS.md`: `PHASE: 3-DEVELOP`, `STATUS: in-progress` while
  working, `done` only once the full test suite for this use case passes.
