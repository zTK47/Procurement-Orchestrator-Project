---
name: ai-sdlc-1-specify
description: Write the acceptance criteria for a use case before any code is written.
---

# PHASE 1 — SPECIFY

## Goal
Answer: "What must the change do?" Produce `docs/specs/UC-XXX-<name>.md`
with Given/When/Then acceptance criteria, BEFORE any implementation.

## Steps
1. Identify the actor and the use case name (matches a class in
   `application/use_cases/`).
2. Write the intent in 1-2 sentences.
3. Write Given/When/Then acceptance criteria covering: the happy path, and
   every domain error the use case can raise.
4. If the use case touches a business rule listed in `docs/PROJECT.md`
   ("Business rules"), the spec must reference which rule.

## Rules
- No code changes in this phase.
- A spec is not "done" until it covers both success and failure paths.
- Update `docs/TASKS.md`: `PHASE: 1-SPECIFY`.
