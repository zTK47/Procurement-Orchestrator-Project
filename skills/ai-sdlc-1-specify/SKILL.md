---
name: ai-sdlc-1-specify
description: Write one use-case specification with testable acceptance criteria before any code.
---

# 1 SPECIFY — What must the change do?

1. Load `docs/TASKS.md`, `docs/PROJECT.md`.
2. Write one `docs/specs/UC-NNN-name.md` from `docs/specs/UC-TEMPLATE.md`: Intent, Actors, Preconditions, Flow, Errors, Acceptance, Tests.
3. Cover the normal flow and every domain error the use case can raise. State IN/OUT scope.
4. Map each acceptance criterion to a unit, integration or e2e test intent.
5. No implementation. Record `PHASE: 1` and the active UC in `docs/TASKS.md`.
