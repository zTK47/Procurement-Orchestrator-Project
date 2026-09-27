"""HTTP endpoints for the procurement pipeline.

Dependency Injection: every route receives concrete repository/adapter
implementations via FastAPI's `Depends`, resolved in
interfaces/api/dependencies.py. Routes only ever depend on the abstract
ports through the use cases they construct -- never on SQLAlchemy directly.
"""
from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException

from procurement.application.ports.llm_adapter import LLMAdapter
from procurement.application.ports.repositories import (
    ApprovalRepository,
    CatalogItemRepository,
    CostCenterRepository,
    ProcurementRequestRepository,
    SupplierRepository,
    UserRepository,
)
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
from procurement.domain.entities import ProcurementRequest
from procurement.domain.exceptions import DomainError
from procurement.domain.value_objects import SKU
from procurement.interfaces.api.dependencies import (
    get_approval_repository,
    get_catalog_repository,
    get_cost_center_repository,
    get_llm_adapter,
    get_procurement_repository,
    get_supplier_repository,
    get_user_repository,
)
from procurement.interfaces.api.schemas import (
    CreateProcurementRequestIn,
    ProcurementRequestOut,
    RecordApprovalDecisionIn,
    SubmitCatalogSelectionIn,
)

router = APIRouter(prefix="/procurement-requests", tags=["procurement"])


def _to_out(request: ProcurementRequest) -> ProcurementRequestOut:
    parsed_out = None
    if request.parsed_data:
        parsed_out = {
            "quantity": request.parsed_data.quantity,
            "product_name": request.parsed_data.product_name,
            "category": request.parsed_data.category,
            "confidence": request.parsed_data.confidence,
        }
    return ProcurementRequestOut(
        request_id=request.id,
        status=request.status.value,
        raw_text=request.raw_text,
        parsed_data=parsed_out,
        resolved_sku=request.resolved_sku.value if request.resolved_sku else None,
        resolved_supplier_id=request.resolved_supplier_id,
        amount=str(request.amount.amount) if request.amount else None,
        currency=request.amount.currency if request.amount else None,
        stock_check=request.stock_check,
        budget_check=request.budget_check,
        required_approval_levels=[lvl.value for lvl in request.required_approval_levels],
        history=[s.value for s in request.history],
    )


def _get_or_404(repo: ProcurementRequestRepository, request_id: str) -> ProcurementRequest:
    procurement_request = repo.get_by_id(request_id)
    if procurement_request is None:
        raise HTTPException(status_code=404, detail="ProcurementRequest not found.")
    return procurement_request


# -- Intake mode 1: free text (parsed by the LLM adapter) --------------------

@router.post("", response_model=ProcurementRequestOut, status_code=201)
def create_from_text(
    payload: CreateProcurementRequestIn,
    procurement_repository: ProcurementRequestRepository = Depends(get_procurement_repository),
    llm_adapter: LLMAdapter = Depends(get_llm_adapter),
) -> ProcurementRequestOut:
    procurement_request = ProcurementRequest(
        id=str(uuid.uuid4()),
        requester_id=payload.requester_id,
        cost_center_id=payload.cost_center_id,
        raw_text=payload.raw_text,
    )
    use_case = ParseRequestUseCase(llm_adapter=llm_adapter, procurement_repository=procurement_repository)
    try:
        result = use_case.execute(procurement_request)
    except DomainError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return _to_out(result)


# -- Intake mode 2: direct catalog selection ---------------------------------

@router.post("/from-catalog", response_model=ProcurementRequestOut, status_code=201)
def create_from_catalog(
    payload: SubmitCatalogSelectionIn,
    procurement_repository: ProcurementRequestRepository = Depends(get_procurement_repository),
    catalog_repository: CatalogItemRepository = Depends(get_catalog_repository),
    supplier_repository: SupplierRepository = Depends(get_supplier_repository),
) -> ProcurementRequestOut:
    procurement_request = ProcurementRequest(
        id=str(uuid.uuid4()), requester_id=payload.requester_id, cost_center_id=payload.cost_center_id,
    )
    use_case = SubmitCatalogSelectionUseCase(
        catalog_repository=catalog_repository,
        supplier_repository=supplier_repository,
        procurement_repository=procurement_repository,
    )
    try:
        result = use_case.execute(procurement_request, SKU(payload.sku), payload.quantity)
    except DomainError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return _to_out(result)


@router.post("/{request_id}/resolve", response_model=ProcurementRequestOut)
def resolve(
    request_id: str,
    procurement_repository: ProcurementRequestRepository = Depends(get_procurement_repository),
    catalog_repository: CatalogItemRepository = Depends(get_catalog_repository),
    supplier_repository: SupplierRepository = Depends(get_supplier_repository),
) -> ProcurementRequestOut:
    procurement_request = _get_or_404(procurement_repository, request_id)
    use_case = ResolveItemUseCase(
        catalog_repository=catalog_repository,
        supplier_repository=supplier_repository,
        procurement_repository=procurement_repository,
    )
    try:
        result = use_case.execute(procurement_request)
    except DomainError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return _to_out(result)


@router.post("/{request_id}/validate", response_model=ProcurementRequestOut)
def validate(
    request_id: str,
    procurement_repository: ProcurementRequestRepository = Depends(get_procurement_repository),
    cost_center_repository: CostCenterRepository = Depends(get_cost_center_repository),
) -> ProcurementRequestOut:
    procurement_request = _get_or_404(procurement_repository, request_id)
    use_case = ValidateRequestUseCase(
        cost_center_repository=cost_center_repository,
        procurement_repository=procurement_repository,
    )
    try:
        result = use_case.execute(procurement_request)
    except DomainError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return _to_out(result)


@router.post("/{request_id}/create-order", response_model=ProcurementRequestOut)
def create_order(
    request_id: str,
    procurement_repository: ProcurementRequestRepository = Depends(get_procurement_repository),
) -> ProcurementRequestOut:
    procurement_request = _get_or_404(procurement_repository, request_id)
    use_case = CreateOrderUseCase(procurement_repository=procurement_repository)
    try:
        result = use_case.execute(procurement_request)
    except DomainError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return _to_out(result)


@router.post("/{request_id}/approvals", response_model=ProcurementRequestOut)
def record_approval_decision(
    request_id: str,
    payload: RecordApprovalDecisionIn,
    procurement_repository: ProcurementRequestRepository = Depends(get_procurement_repository),
    approval_repository: ApprovalRepository = Depends(get_approval_repository),
    cost_center_repository: CostCenterRepository = Depends(get_cost_center_repository),
    user_repository: UserRepository = Depends(get_user_repository),
) -> ProcurementRequestOut:
    procurement_request = _get_or_404(procurement_repository, request_id)
    use_case = RecordApprovalDecisionUseCase(
        procurement_repository=procurement_repository,
        approval_repository=approval_repository,
        cost_center_repository=cost_center_repository,
        user_repository=user_repository,
    )
    try:
        result = use_case.execute(
            request=procurement_request,
            approver_id=payload.approver_id,
            level=payload.level,
            decision=payload.decision,
        )
    except DomainError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return _to_out(result)


@router.get("/{request_id}", response_model=ProcurementRequestOut)
def get_request(
    request_id: str,
    procurement_repository: ProcurementRequestRepository = Depends(get_procurement_repository),
) -> ProcurementRequestOut:
    return _to_out(_get_or_404(procurement_repository, request_id))
