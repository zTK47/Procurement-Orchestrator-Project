---
name: ai-sdlc-3-develop
description: Implement the active use case test-first (Red, Green, Refactor).
---

# 3 DEVELOP — Does the implementation satisfy the tests?

1. Write or extend integration tests for boundary behavior (repositories, API).
2. Write or extend unit tests for domain rules and use-case logic. Run them: they must fail for the right reason (Red).
3. Implement the smallest change that passes (Green). Commit tests and code so the red → green step is visible in history.
4. Refactor with the suite green.
5. Extend existing tests and files before creating new ones. Run the relevant tests after each step.

Rules: tests before code; keep `domain/` and `application/` free of FastAPI, Pydantic, SQLAlchemy; LLM and ERP only through ports; if a requirement is unclear, ask. Record `PHASE: 3`; `done` only when the UC's tests pass.
