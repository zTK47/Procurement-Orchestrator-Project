# UC-006 — Record Approval Decision

**Use case:** `RecordApprovalDecisionUseCase`

## Intent
Not part of the original prompt's 4 use cases, but required to actually
complete the workflow the brainstorm's state diagram describes
(`PENDING_APPROVAL -> APPROVED -> ORDER_SENT -> ...`). Records one
approver's decision at one level, and — once every required level is
approved — performs the final, authoritative budget check and deducts the
cost center's budget.

## Acceptance Criteria

- **Given** a user without the role matching the approval level
  **When** they attempt to record a decision
  **Then** `UnauthorizedApproverError` is raised.

- **Given** an approver who already recorded a decision at this level for
  this request
  **When** they attempt to record another one
  **Then** `DuplicateApprovalError` is raised.

- **Given** a request requiring both `MANAGER` and `BUDGET_OWNER` approval,
  with only `MANAGER` approved so far
  **When** the manager's approval is recorded
  **Then** the request stays `PENDING_APPROVAL`.

- **Given** all required levels are now `APPROVED` and the cost center still
  has enough budget
  **When** the last approval is recorded
  **Then** the cost center's `budget_spent` is increased by the request's
  amount and the request moves to `APPROVED`.

- **Given** all required levels are approved but the cost center's budget
  has since been consumed elsewhere
  **When** the last approval is recorded
  **Then** `BudgetExceededError` is raised (request stays `PENDING_APPROVAL`).

- **Given** any approver rejects at their level
  **When** the decision is recorded
  **Then** the whole request moves to `REJECTED` (terminal).
