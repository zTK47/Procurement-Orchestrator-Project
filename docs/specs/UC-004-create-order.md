# UC-004 — Create Order

**Use case:** `CreateOrderUseCase`
**Domain service:** `ApprovalRoutingPolicy`

## Intent
Given a `VALIDATED` request, decide how many levels of human approval it
needs (based on amount thresholds) and transition it accordingly.

## Approval Routing Policy (rule 1)
- amount ≤ manager_threshold (default 1000) → no approval needed.
- manager_threshold < amount ≤ budget_owner_threshold (default 10000) →
  `MANAGER` approval required.
- amount > budget_owner_threshold → `MANAGER` **and** `BUDGET_OWNER`
  approval required.

## Acceptance Criteria

- **Given** a validated request with amount ≤ manager_threshold
  **When** creating the order
  **Then** the request moves straight to `APPROVED`, no approvals required.

- **Given** a validated request with amount above manager_threshold but at
  or below budget_owner_threshold
  **When** creating the order
  **Then** the request moves to `PENDING_APPROVAL` with
  `required_approval_levels = [MANAGER]`.

- **Given** a validated request with amount above budget_owner_threshold
  **When** creating the order
  **Then** `required_approval_levels = [MANAGER, BUDGET_OWNER]`.
