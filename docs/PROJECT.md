# Procurement Orchestrator — Project Context

## Purpose

Turns a purchase need, given as free text or as a direct catalog selection, into
a validated, approved and ERP-booked purchase order. The system enforces sourcing,
budget validation, threshold-based approval and the order hand-off to an ERP.

Course: FHNW BSc Business Information Technology, *AI-assisted Software
Development*, capstone project (team of 2). The process (AI-SDLC, TDD, Clean
Architecture, coding-agent use) matters more than the application.

## Architecture

Clean Architecture, dependencies point inward:
`domain ← application ← interfaces ← infrastructure`

| Layer | Contents | Validated by |
|---|---|---|
| `domain/` | Entities, value objects, domain services, domain errors. Pure Python. | Unit tests |
| `application/` | Use cases, ports (repositories, `LLMAdapter`, `ErpGateway`), JSON contract builder. | Unit tests |
| `interfaces/` | FastAPI router, Pydantic DTOs, `Depends` wiring, static frontend. | Integration + e2e tests |
| `infrastructure/` | SQLAlchemy models and repositories, mock LLM and ERP adapters, in-memory repositories, seed data, app startup. | Integration + e2e tests |

Concrete adapters are chosen in one place, `interfaces/api/dependencies.py`.
Related decisions: see `docs/adr/` (all currently Proposed).

## Structure

```
src/procurement/{domain,application,interfaces,infrastructure}/
tests/{unit,integration,e2e}/
docs/{PROJECT.md,TASKS.md,LEARNINGS.md,specs/,adr/}
skills/ai-sdlc-{0..5}-*/SKILL.md
scripts/setup-skills.sh
demo.py            # full pipeline, no dependencies needed
```

## Domain model

Entities: `User`, `CostCenter`, `Supplier`, `CatalogItem`, `ProcurementRequest`
(aggregate root), `Approval`. Value objects: `Money`, `SKU`, `ParsedRequest`.
Domain services: `SourcingRule` (Sourcing Funnel), `ApprovalRoutingPolicy`.

Business rules:
1. Approval routing: amount ≤ 1000 no approval; > 1000 `MANAGER`; > 10000 also `BUDGET_OWNER`.
2. Budget is checked when validating and again, authoritatively, right before it is spent.
3. Sourcing Funnel: approved supplier, enough stock, lead time ≤ 14 days, cheapest wins;
   a price tie raises `RequiresClarificationError` (ADR-002).
4. `REJECTED` and `COMPLETED` are terminal; an approved request cannot be re-decided.
5. The same approver cannot decide twice at the same level.
6. An order can only be sent to the ERP after approval; goods receipt only after the order was sent.

## Workflow

```
CREATED → PARSED → RESOLVED → VALIDATED → PENDING_APPROVAL → APPROVED
   → ORDER_SENT → GOODS_RECEIPT → COMPLETED
VALIDATED → APPROVED (no approval required)      PENDING_APPROVAL → REJECTED
```

| Use case | Transition |
|---|---|
| UC-001 Parse Request | CREATED → PARSED |
| UC-002 Resolve Item | PARSED → RESOLVED |
| UC-005 Submit Catalog Selection | CREATED → RESOLVED (via a synthetic PARSED step) |
| UC-003 Validate Request | RESOLVED → VALIDATED |
| UC-004 Create Order | VALIDATED → PENDING_APPROVAL or APPROVED |
| UC-006 Record Approval Decision | PENDING_APPROVAL → APPROVED or REJECTED |
| UC-007 Send Order To ERP | APPROVED → ORDER_SENT |
| UC-008 Record Goods Receipt | ORDER_SENT → GOODS_RECEIPT |
| UC-009 Complete Request | GOODS_RECEIPT → COMPLETED |

## API contract

Every endpoint returns the pipeline JSON: `requestId`, `status`, `rawText`,
`parsedData`, `resolvedData`, `validation`, `workflow` (`currentState`,
`nextState`, `history`). Additions to the original sketch: `resolvedData.totalAmount`,
`validation.approvalLevels` (`approvalLevel` is the highest required level) and `erpReference`.
`requiresApproval` is `null` until UC-004 has decided it.

## Commands

```bash
python demo.py                                   # pipeline without any install
pip install -e ".[dev]"                          # dependencies (also in requirements.txt)
docker compose up -d db                          # local Postgres
pytest tests/unit                                # domain + application + mock adapters, no DB
pytest tests/integration                         # repositories against Postgres
pytest tests/e2e                                 # full HTTP stack
ruff check src tests
uvicorn procurement.infrastructure.main:app --reload   # UI on /, Swagger on /docs
docker build -t procurement-orchestrator . && docker compose up
bash scripts/setup-skills.sh claude              # expose skills/ to an agent
```

## Dependencies

Python 3.12; runtime: FastAPI, Uvicorn, Pydantic v2, SQLAlchemy 2, psycopg2;
dev: pytest, httpx, ruff. Database: PostgreSQL (Neon free tier in production).
Deployment target: Render (Docker web service) — see `skills/ai-sdlc-5-deploy`.

## Scope

In: free-text and catalog intake, mock LLM, mock ERP, approval workflow.
Out (Future Work): OCI Punchout (ADR-005), real LLM via LiteLLM, real SAP adapter,
configurable procurement strategy for price ties, partial stock / backorder.
