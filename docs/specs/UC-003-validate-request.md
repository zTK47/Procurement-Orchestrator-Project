# UC-003 — Validate Request

**Use case:** `ValidateRequestUseCase`

## Intent
Check that the resolved request's amount fits within its cost center's
remaining budget. Scope is deliberately narrow (budget only) — approval
routing is a separate concern, handled by UC-004 (`CreateOrderUseCase`).

## Acceptance Criteria

- **Given** a `RESOLVED` request whose amount is within the cost center's
  available budget
  **When** validating
  **Then** the request moves to `VALIDATED`, `budget_check = "PASSED"`, and
  `required_approval_levels` is left untouched (empty — not yet decided).

- **Given** a `RESOLVED` request whose amount exceeds the cost center's
  available budget
  **When** validating
  **Then** `BudgetExceededError` is raised and the request status does not
  change (stays `RESOLVED`).
