# ADR-001: Adopt Clean Architecture (Domain/Application/Interfaces/Infrastructure)

**Status:** Accepted (24.09.2026)

## Context
The course requires an enterprise-grade architecture separating business
logic from framework code, and a testable domain model.

## Decision
Adopt Clean Architecture with 4 layers. Dependency Rule: dependencies point
only inward (`infrastructure -> interfaces -> application -> domain`).
`domain/` has zero third-party imports.

## Consequences
- Domain and Application layers can be fully unit-tested without a database
  or web framework (see 44 passing unit tests with zero DB dependency).
- Swapping the in-memory repositories for SQLAlchemy-backed ones (Phase 4)
  requires no change to domain/application code.
- Slightly more boilerplate (explicit ports/ABCs) than a simple layered
  script — accepted as the cost of testability and the course's explicit
  grading criteria.
