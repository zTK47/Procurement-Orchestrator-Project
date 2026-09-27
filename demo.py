#!/usr/bin/env python3
"""Runs the full Procurement Orchestrator pipeline end-to-end, in-memory,
with zero external dependencies (no FastAPI, no DB required).

Demonstrates BOTH intake modes from the original brainstorm:
  1. Free text  -> ParseRequestUseCase + ResolveItemUseCase
  2. Catalog    -> SubmitCatalogSelectionUseCase (skips parsing/sourcing)

(The third mode, OCI Punchout, is out of scope -- see docs/PROJECT.md.)

Usage:
    python demo.py
"""
from __future__ import annotations

import json
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from procurement.application.use_cases.create_order import CreateOrderUseCase
from procurement.application.use_cases.parse_request import ParseRequestUseCase
from procurement.application.use_cases.record_approval_decision import (
    RecordApprovalDecisionUseCase,
)
from procurement.application.use_cases.resolve_item import ResolveItemUseCase
from procurement.application.use_cases.submit_catalog_selection import (
    SubmitCatalogSelectionUseCase,
)
from procurement.application.use_cases.validate_request import ValidateRequestUseCase
from procurement.domain.entities import ApprovalDecision, ApprovalLevel, ProcurementRequest
from procurement.domain.value_objects import SKU
from procurement.infrastructure.in_memory_repositories import (
    InMemoryApprovalRepository,
    InMemoryCatalogItemRepository,
    InMemoryCostCenterRepository,
    InMemoryProcurementRequestRepository,
    InMemorySupplierRepository,
    InMemoryUserRepository,
)
from procurement.infrastructure.mock_llm_adapter import MockLLMAdapter
from procurement.infrastructure.seed_data import build_seed_data


def to_contract_json(request: ProcurementRequest) -> dict:
    return {
        "requestId": request.id,
        "status": request.status.value,
        "rawText": request.raw_text,
        "parsedData": {
            "quantity": request.parsed_data.quantity,
            "productName": request.parsed_data.product_name,
            "category": request.parsed_data.category,
            "confidence": request.parsed_data.confidence,
        } if request.parsed_data else None,
        "resolvedData": {
            "sku": request.resolved_sku.value,
            "supplierId": request.resolved_supplier_id,
            "unitPrice": str(request.amount.amount / request.parsed_data.quantity),
            "currency": request.amount.currency,
        } if request.resolved_sku and request.amount and request.parsed_data else None,
        "validation": {
            "budgetCheck": request.budget_check,
            "stockCheck": request.stock_check,
            "requiresApproval": bool(request.required_approval_levels),
            "approvalLevels": [lvl.value for lvl in request.required_approval_levels],
        },
        "workflow": {
            "currentState": request.status.value,
            "history": [s.value for s in request.history],
        },
    }


def run_free_text_pipeline(repos, llm_adapter) -> ProcurementRequest:
    (procurement_repository, catalog_repository, supplier_repository,
     cost_center_repository, user_repository, approval_repository) = repos

    raw_text = "I need 5 new Lenovo Laptops for the IT department"
    print(f"\n{'='*70}\nSCENARIO A: Free-text intake\n{'='*70}")
    print(f"Raw request: {raw_text!r}\n")

    request = ProcurementRequest(
        id=str(uuid.uuid4()), requester_id="U-REQ-1", cost_center_id="CC-IT", raw_text=raw_text,
    )
    request = ParseRequestUseCase(llm_adapter, procurement_repository).execute(request)
    print(f"[1] Parsed    -> status={request.status.value}, category={request.parsed_data.category!r}")

    request = ResolveItemUseCase(catalog_repository, supplier_repository, procurement_repository).execute(request)
    print(f"[2] Resolved  -> status={request.status.value}, sku={request.resolved_sku.value}, amount={request.amount}")

    request = ValidateRequestUseCase(cost_center_repository, procurement_repository).execute(request)
    print(f"[3] Validated -> status={request.status.value}, budget_check={request.budget_check}")

    request = CreateOrderUseCase(procurement_repository).execute(request)
    print(f"[4] Order     -> status={request.status.value}, required_levels={[l.value for l in request.required_approval_levels]}")

    for level in request.required_approval_levels:
        approver_id = "U-MAN-1" if level == ApprovalLevel.MANAGER else "U-BO-1"
        request = RecordApprovalDecisionUseCase(
            procurement_repository, approval_repository, cost_center_repository, user_repository
        ).execute(request, approver_id, level, ApprovalDecision.APPROVED)
        print(f"[5] Approval  -> {level.value} approved, status={request.status.value}")

    print("\nFinal JSON contract:")
    print(json.dumps(to_contract_json(request), indent=2))
    return request


def run_catalog_selection_pipeline(repos) -> ProcurementRequest:
    (procurement_repository, catalog_repository, supplier_repository,
     cost_center_repository, _user_repository, _approval_repository) = repos

    print(f"\n{'='*70}\nSCENARIO B: Direct catalog selection intake\n{'='*70}")
    print("User directly picks SKU=LEN-T14-G3, quantity=2\n")

    request = ProcurementRequest(id=str(uuid.uuid4()), requester_id="U-REQ-1", cost_center_id="CC-IT")
    request = SubmitCatalogSelectionUseCase(
        catalog_repository, supplier_repository, procurement_repository
    ).execute(request, SKU("LEN-T14-G3"), quantity=2)
    print(f"[1] Resolved directly -> status={request.status.value}, amount={request.amount}, stock_check={request.stock_check}")

    request = ValidateRequestUseCase(cost_center_repository, procurement_repository).execute(request)
    request = CreateOrderUseCase(procurement_repository).execute(request)
    print(f"[2] Validated + Order -> status={request.status.value}")
    return request


def main() -> None:
    suppliers, catalog_items, cost_centers, users = build_seed_data()
    repos = (
        InMemoryProcurementRequestRepository(),
        InMemoryCatalogItemRepository(catalog_items),
        InMemorySupplierRepository(suppliers),
        InMemoryCostCenterRepository(cost_centers),
        InMemoryUserRepository(users),
        InMemoryApprovalRepository(),
    )

    run_free_text_pipeline(repos, MockLLMAdapter())
    run_catalog_selection_pipeline(repos)

    final_cost_center = repos[3].get_by_id("CC-IT")
    print(f"\n{'='*70}\nCost center CC-IT total budget spent: "
          f"{final_cost_center.budget_spent.amount} {final_cost_center.budget_spent.currency}")


if __name__ == "__main__":
    main()
