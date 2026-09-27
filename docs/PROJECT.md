# Procurement Orchestrator — Project Reference

## Purpose

Turns a purchase need — expressed either as free text or a direct catalog
selection — into a validated, approved purchase order, enforcing real
business rules end-to-end: sourcing, budget validation, and a multi-level
approval workflow.

Course context: FHNW BSc Business Information Technology, module
"AI-assisted Software Development", capstone project.

## Architecture

Clean Architecture, 4 layers. The Dependency Rule: dependencies point only
inward. `domain/` imports nothing from the other three layers and no
third-party package.

```
domain/            <- pure Python. Entities, Value Objects, domain services.
  entities.py         User, CostCenter, Supplier, CatalogItem,
                       ProcurementRequest (state machine), Approval
  value_objects.py    Money, SKU, ParsedRequest (immutable, frozen)
  exceptions.py       Domain errors (business rule violations)
  services/
    sourcing_rules.py         SourcingRule (the Sourcing Funnel)
    approval_routing_policy.py ApprovalRoutingPolicy (threshold rules)

application/       <- orchestrates domain objects; knows only domain + ports
  ports/              abstract repository interfaces (ABCs) + LLMAdapter
  use_cases/          ParseRequestUseCase, ResolveItemUseCase,
                       ValidateRequestUseCase, CreateOrderUseCase,
                       SubmitCatalogSelectionUseCase,
                       RecordApprovalDecisionUseCase

interfaces/        <- FastAPI routers + Pydantic DTOs. Validation lives here.
  api/

infrastructure/    <- concrete, technical. SQLAlchemy, FastAPI wiring, the
                      mock LLM adapter, in-memory repositories.
  main.py             the ONLY place concrete classes are instantiated and
                       injected into use cases (Dependency Injection)
```

## Domain Model (6 entities)

| Entity | Key attributes |
|---|---|
| User | id, name, email, role (`REQUESTER`, `MANAGER`, `BUDGET_OWNER`) |
| CostCenter | id, name, budget_total, budget_spent (both `Money`) |
| Supplier | id, name, approved |
| CatalogItem | id, sku, product_name, category, supplier_id, unit_price, stock_qty, lead_time_days |
| ProcurementRequest | id, requester_id, cost_center_id, raw_text, parsed_data, resolved_sku, amount, status, history (aggregate root) |
| Approval | id, procurement_request_id, approver_id, level, decision, decided_at |

Value Objects (immutable): `Money`, `SKU`, `ParsedRequest`.

## Business Rules (domain invariants)

1. **Approval routing** (`ApprovalRoutingPolicy`): amount ≤ 1000 → no
   approval; > 1000 → `MANAGER`; > 10000 → also `BUDGET_OWNER`.
2. **Budget check** (`CostCenter.has_available_budget`, enforced twice — a
   pre-check in `ValidateRequestUseCase` and a final, authoritative check in
   `RecordApprovalDecisionUseCase` right before spending, since budget may
   change between the two).
3. **Price-tie clarification** (`SourcingRule`): a tie for the cheapest
   approved, in-stock catalog item raises `RequiresClarificationError`
   rather than picking one silently (see ADR-002 — currently `Proposed`,
   pending team confirmation).
4. **Terminal states**: `APPROVED`/`REJECTED` requests cannot be modified or
   re-approved (enforced by the `ProcurementRequest` state machine).
5. **No duplicate approvals**: the same approver cannot record two
   decisions at the same level for the same request.

## Workflow State Machine

```
CREATED -> PARSED -> RESOLVED -> VALIDATED -> PENDING_APPROVAL -> APPROVED
                                      \-----------------------------^ (if no approval required)
PENDING_APPROVAL -> REJECTED (terminal)
APPROVED -> ORDER_SENT -> GOODS_RECEIPT -> COMPLETED
```

Two intake paths reach `RESOLVED` differently:
- **Free text**: `CREATED -[ParseRequestUseCase]-> PARSED -[ResolveItemUseCase]-> RESOLVED`
- **Direct catalog selection**: `CREATED -[SubmitCatalogSelectionUseCase]-> PARSED -> RESOLVED` (in one call — no LLM/sourcing ranking involved, since the item is already chosen)

Both then continue identically:
`RESOLVED -[ValidateRequestUseCase]-> VALIDATED -[CreateOrderUseCase]-> (PENDING_APPROVAL | APPROVED) -[RecordApprovalDecisionUseCase]-> (APPROVED | REJECTED)`

## Use Cases

1. `ParseRequestUseCase` — free text → `ParsedRequest` (via `LLMAdapter`).
2. `ResolveItemUseCase` — `ParsedRequest` → `CatalogItem` (via `SourcingRule`).
3. `ValidateRequestUseCase` — budget check only.
4. `CreateOrderUseCase` — determines approval levels, transitions to
   `PENDING_APPROVAL`/`APPROVED`.
5. `SubmitCatalogSelectionUseCase` — direct catalog intake (2nd of the 3
   originally discussed intake modes).
6. `RecordApprovalDecisionUseCase` — records one approver's decision;
   performs the final budget check and deducts the cost center's budget
   once every required level is approved.

## Tech Stack

| Layer | Choice | Rationale |
|---|---|---|
| Language | Python 3.12 | Lecture examples, strong agent/LLM code-gen support |
| API | FastAPI | Course-recommended Clean Architecture template |
| ORM | SQLAlchemy 2.0 | De facto standard Python ORM |
| DB | PostgreSQL (Neon free tier) | Course-recommended, zero-cost |
| Validation | Pydantic v2 | Native FastAPI integration; kept out of domain/application |
| Testing | pytest + httpx | Standard, agent-friendly |
| Containerization | Docker | Required for Render deployment |
| Deployment | Render (Docker Web Service) | Course-recommended, free tier |
| CI/CD | GitHub Actions | lint → unit → integration → docker build |
| Coding agent | GitHub Copilot (evaluating Claude Code/Codex CLI) | Course-provided access |

## Future Work (explicitly out of scope for this prototype)

- **OCI Punchout catalog integration** (see ADR-005): a third intake mode
  from the original brainstorm, requiring an external hosted-catalog
  session and cXML authentication. Deliberately excluded to keep the
  deliverable achievable within the course timeline.
- Real LLM provider behind `LLMAdapter` (via LiteLLM), replacing
  `MockLLMAdapter` (see ADR-004).
- SQLAlchemy-backed repositories replacing the in-memory ones (scaffolding
  already present in `infrastructure/db.py` and `infrastructure/models.py`).
- Partial-stock / backorder handling (currently `stock_check` is a strict
  gate, not a partial-fulfillment mechanism).
