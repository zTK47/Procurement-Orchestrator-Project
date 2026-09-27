---
name: ai-sdlc-2-design
description: Decide where behavior belongs (which layer, which entity/service) and record consequential decisions as ADRs.
---

# PHASE 2 — DESIGN

## Goal
Answer: "Where does behavior belong?" Decide which layer/entity/service
owns each rule from the spec, before writing tests or code.

## Steps
1. For each acceptance criterion in the spec, identify: does this belong in
   `domain/` (a business rule/invariant), `application/` (orchestration of
   a use case), `interfaces/` (request/response shaping), or
   `infrastructure/` (a technical detail)?
2. If the decision is consequential (affects multiple use cases, changes an
   existing contract, or deviates from an earlier plan/brainstorm), write an
   ADR in `docs/adr/` with `Status: Proposed`.
3. Do NOT mark an ADR `Accepted` yourself — that requires an explicit human
   team decision (see AGENTS.md "Architecture Gates").

## Rules
- Domain rules never leak into `interfaces/` or `infrastructure/`.
- Update `docs/TASKS.md`: `PHASE: 2-DESIGN`.
