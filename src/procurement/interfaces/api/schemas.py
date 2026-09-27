"""Pydantic schemas (DTOs). Validation lives ONLY here and in the
infrastructure layer -- never in domain or application."""
from __future__ import annotations

from pydantic import BaseModel, Field

from procurement.domain.entities import ApprovalDecision, ApprovalLevel


class CreateProcurementRequestIn(BaseModel):
    requester_id: str
    cost_center_id: str
    raw_text: str = Field(..., min_length=1)


class ParsedDataOut(BaseModel):
    quantity: int
    product_name: str
    category: str
    confidence: float


class SubmitCatalogSelectionIn(BaseModel):
    requester_id: str
    cost_center_id: str
    sku: str
    quantity: int = Field(..., gt=0)


class ProcurementRequestOut(BaseModel):
    request_id: str
    status: str
    raw_text: str | None
    parsed_data: ParsedDataOut | None = None
    resolved_sku: str | None = None
    resolved_supplier_id: str | None = None
    amount: str | None = None
    currency: str | None = None
    stock_check: str | None = None
    budget_check: str | None = None
    required_approval_levels: list[str] = []
    history: list[str]


class RecordApprovalDecisionIn(BaseModel):
    approver_id: str
    level: ApprovalLevel
    decision: ApprovalDecision
