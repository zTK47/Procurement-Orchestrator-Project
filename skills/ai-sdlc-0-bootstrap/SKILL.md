---
name: ai-sdlc-0-bootstrap
description: Initialize project scaffolding, folder structure, and tooling for a new use case or the project itself.
---

# PHASE 0 — BOOTSTRAP

## Goal
Answer: "What are we building?" Set up structure so later phases have
somewhere to put their output.

## Steps
1. Confirm the folder structure matches `docs/PROJECT.md` (domain/
   application/interfaces/infrastructure, tests/unit/integration/e2e,
   docs/specs, docs/adr).
2. If bootstrapping a brand-new use case: create an empty
   `docs/specs/UC-XXX-<name>.md` stub (do not fill it in yet — that is
   Phase 1) and add a line to `docs/TASKS.md` backlog.
3. Do NOT write implementation code in this phase.

## Rules
- Never skip straight to Phase 3 (Develop) for a new use case or entity.
- Update `docs/TASKS.md`: `PHASE: 0-BOOTSTRAP`, `STATUS: done` once the
  structure exists and is committed.
