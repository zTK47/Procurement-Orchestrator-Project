---
name: ai-sdlc-2-design
description: Decide where behavior belongs and record consequential architecture decisions as ADRs.
---

# 2 DESIGN — Where does behavior belong?

1. Read the active UC and `docs/PROJECT.md`.
2. Place each rule in `domain/`, `application/`, `interfaces/` or `infrastructure/`; define ports and adapters.
3. Slice the work into small vertical tasks in `docs/TASKS.md`; list the tests needed per boundary.
4. Only for a consequential choice, create `docs/adr/ADR-NNN-short-title.md` with: Status, Context, Alternatives, Decision, Consequences. Status starts as **Proposed**.
5. An ADR becomes Accepted only when a named team member accepts it, with a review reference. An agent proposal is not approval.
6. Reflect accepted decisions in `docs/PROJECT.md` and, if they become durable rules, in `AGENTS.md` (human review).
7. No code and no tests in this phase. Record `PHASE: 2`.
