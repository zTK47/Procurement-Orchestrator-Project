# ADR-003: Dependency Injection via abstract repository/adapter ports

**Status:** Accepted (24.09.2026)

## Context
Use cases need to read/write data (procurement requests, catalog items,
suppliers, cost centers, users, approvals) and call an LLM, but must not be
coupled to a specific database or LLM provider (Dependency Inversion
Principle, covered in Lecture 2).

## Decision
Define abstract base classes (`application/ports/repositories.py`,
`application/ports/llm_adapter.py`) that use cases depend on. Concrete
implementations (`InMemory*Repository` today, `SQLAlchemy*Repository` from
Phase 4 on; `MockLLMAdapter` today, a LiteLLM-backed adapter later) are
instantiated and injected only in `infrastructure/main.py`.

## Consequences
- Use cases (e.g. `SubmitCatalogSelectionUseCase`) are tested with
  `InMemory*` implementations acting as fast, deterministic fakes — no
  mocking framework needed.
- Switching persistence technology or LLM provider touches only
  `infrastructure/` and one line in `main.py`'s wiring.
