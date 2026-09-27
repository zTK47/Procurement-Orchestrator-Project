"""Domain entities for the Procurement Orchestrator.

Pure Python only: no Pydantic, no SQLAlchemy, no framework imports.
Entities have identity (an `id`) and encapsulate the business rules that
protect their own invariants.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from procurement.domain.exceptions import (
    IllegalStatusTransitionError,
)
from procurement.domain.value_objects import Money, ParsedRequest, SKU


# --------------------------------------------------------------------------
# Enums
# --------------------------------------------------------------------------

class UserRole(str, Enum):
    REQUESTER = "REQUESTER"
    MANAGER = "MANAGER"
    BUDGET_OWNER = "BUDGET_OWNER"


class ProcurementStatus(str, Enum):
    CREATED = "CREATED"
    PARSED = "PARSED"
    RESOLVED = "RESOLVED"
    VALIDATED = "VALIDATED"
    PENDING_APPROVAL = "PENDING_APPROVAL"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    ORDER_SENT = "ORDER_SENT"
    GOODS_RECEIPT = "GOODS_RECEIPT"
    COMPLETED = "COMPLETED"


class ApprovalLevel(str, Enum):
    MANAGER = "MANAGER"
    BUDGET_OWNER = "BUDGET_OWNER"


class ApprovalDecision(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


# The workflow state machine (slide-documented in docs/PROJECT.md).
# Maps: current status -> set of statuses it may legally move to.
_ALLOWED_TRANSITIONS: dict[ProcurementStatus, set[ProcurementStatus]] = {
    ProcurementStatus.CREATED: {ProcurementStatus.PARSED},
    ProcurementStatus.PARSED: {ProcurementStatus.RESOLVED},
    ProcurementStatus.RESOLVED: {ProcurementStatus.VALIDATED},
    ProcurementStatus.VALIDATED: {
        ProcurementStatus.PENDING_APPROVAL,
        ProcurementStatus.APPROVED,  # auto-approved: no approval level required
    },
    ProcurementStatus.PENDING_APPROVAL: {
        ProcurementStatus.APPROVED,
        ProcurementStatus.REJECTED,
    },
    ProcurementStatus.APPROVED: {ProcurementStatus.ORDER_SENT},
    ProcurementStatus.ORDER_SENT: {ProcurementStatus.GOODS_RECEIPT},
    ProcurementStatus.GOODS_RECEIPT: {ProcurementStatus.COMPLETED},
    ProcurementStatus.REJECTED: set(),   # terminal
    ProcurementStatus.COMPLETED: set(),  # terminal
}


# --------------------------------------------------------------------------
# Entities
# --------------------------------------------------------------------------

@dataclass
class User:
    id: str
    name: str
    email: str
    role: UserRole


@dataclass
class CostCenter:
    id: str
    name: str
    budget_total: Money
    budget_spent: Money

    def available_budget(self) -> Money:
        return self.budget_total - self.budget_spent

    def has_available_budget(self, amount: Money) -> bool:
        return self.available_budget() >= amount

    def spend(self, amount: Money) -> None:
        """Deduct `amount` from the available budget.

        Raises ValueError (via Money's own invariant) if this would make
        budget_spent exceed budget_total in a way that produces a negative
        remaining balance beyond what Money allows -- the actual "is there
        enough budget" business check is BudgetExceededError, raised by the
        use case *before* calling spend().
        """
        self.budget_spent = self.budget_spent + amount


@dataclass
class Supplier:
    id: str
    name: str
    approved: bool


@dataclass
class CatalogItem:
    id: str
    sku: SKU
    product_name: str
    category: str
    supplier_id: str
    unit_price: Money
    stock_qty: int
    lead_time_days: int


@dataclass
class Approval:
    id: str
    procurement_request_id: str
    approver_id: str
    level: ApprovalLevel
    decision: ApprovalDecision = ApprovalDecision.PENDING
    decided_at: datetime | None = None


@dataclass
class ProcurementRequest:
    """Aggregate root of the Procurement domain.

    Owns the workflow state machine: any status change must go through
    `transition_to`, which enforces `_ALLOWED_TRANSITIONS`.
    """

    id: str
    requester_id: str
    cost_center_id: str
    raw_text: str | None = None
    parsed_data: ParsedRequest | None = None
    resolved_sku: SKU | None = None
    resolved_supplier_id: str | None = None
    amount: Money | None = None
    stock_check: str | None = None   # "PASSED" | "FAILED" -- set at resolution time
    budget_check: str | None = None  # "PASSED" | "FAILED" -- set at validation time
    required_approval_levels: list[ApprovalLevel] = field(default_factory=list)
    status: ProcurementStatus = ProcurementStatus.CREATED
    history: list[ProcurementStatus] = field(
        default_factory=lambda: [ProcurementStatus.CREATED]
    )

    # -- state machine -----------------------------------------------------

    def transition_to(self, new_status: ProcurementStatus) -> None:
        allowed = _ALLOWED_TRANSITIONS.get(self.status, set())
        if new_status not in allowed:
            raise IllegalStatusTransitionError(
                f"Cannot transition ProcurementRequest {self.id} from "
                f"{self.status.value} to {new_status.value}."
            )
        self.status = new_status
        self.history.append(new_status)

    # -- pipeline steps (each wraps a transition with the relevant data) ---

    def mark_parsed(self, parsed_data: ParsedRequest) -> None:
        self.parsed_data = parsed_data
        self.transition_to(ProcurementStatus.PARSED)

    def mark_resolved(
        self, sku: SKU, supplier_id: str, amount: Money, stock_check: str = "PASSED"
    ) -> None:
        self.resolved_sku = sku
        self.resolved_supplier_id = supplier_id
        self.amount = amount
        self.stock_check = stock_check
        self.transition_to(ProcurementStatus.RESOLVED)

    def mark_validated(self, budget_check: str = "PASSED") -> None:
        """UC-003 (ValidateRequestUseCase): budget check only. Does NOT
        decide approval routing -- that is CreateOrderUseCase's job (UC-004),
        matching the separation of concerns requested in the project brief."""
        self.budget_check = budget_check
        self.transition_to(ProcurementStatus.VALIDATED)

    def submit_for_approval(self, required_approval_levels: list[ApprovalLevel]) -> None:
        """UC-004 (CreateOrderUseCase): determines whether human approval is
        required and transitions accordingly."""
        self.required_approval_levels = required_approval_levels
        if required_approval_levels:
            self.transition_to(ProcurementStatus.PENDING_APPROVAL)
        else:
            self.transition_to(ProcurementStatus.APPROVED)

    def approve(self) -> None:
        self.transition_to(ProcurementStatus.APPROVED)

    def reject(self) -> None:
        self.transition_to(ProcurementStatus.REJECTED)
