"""Entities of the Order PDF Orchestration context. Pure Python, no frameworks."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from order_pdf_orchestration.domain.exceptions import InvalidLineItemError
from order_pdf_orchestration.domain.value_objects import Money


class OrderStatus(str, Enum):
    DRAFT = "DRAFT"
    GENERATED = "GENERATED"
    NEEDS_CLARIFICATION = "NEEDS_CLARIFICATION"
    VALIDATED = "VALIDATED"
    SENT = "SENT"


@dataclass
class Supplier:
    id: str
    name: str
    contact_reference: str


@dataclass
class SupplierOffer:
    id: str
    supplier_id: str
    raw_text: str


@dataclass(frozen=True)
class OrderLineItem:
    id: str
    description: str
    quantity: int
    unit_price: Money

    def __post_init__(self) -> None:
        if not self.description or not self.description.strip():
            raise InvalidLineItemError("Line item description must not be blank.")
        if self.quantity <= 0:
            raise InvalidLineItemError(
                f"Line item '{self.description}' must have a quantity greater than 0."
            )

    def line_total(self) -> Money:
        return self.unit_price.times(self.quantity)


@dataclass
class OrderRequest:
    """Aggregate root."""

    id: str
    supplier_offer_id: str
    prompt_text: str
    line_items: list[OrderLineItem] = field(default_factory=list)
    status: OrderStatus = OrderStatus.DRAFT
    validation_notes: list[str] = field(default_factory=list)
    pdf_reference: str | None = None
    supplier_reference: str | None = None

    def total(self) -> Money | None:
        if not self.line_items:
            return None
        total = Money.zero(self.line_items[0].unit_price.currency)
        for item in self.line_items:
            total = total + item.line_total()
        return total
