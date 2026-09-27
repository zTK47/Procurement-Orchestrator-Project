from decimal import Decimal

import pytest

from procurement.domain.entities import (
    ApprovalLevel,
    ProcurementRequest,
    ProcurementStatus,
)
from procurement.domain.exceptions import IllegalStatusTransitionError
from procurement.domain.value_objects import SKU, Money, ParsedRequest


def make_request() -> ProcurementRequest:
    return ProcurementRequest(id="PR-1", requester_id="U-1", cost_center_id="CC-1")


def test_new_request_starts_in_created_status():
    request = make_request()
    assert request.status == ProcurementStatus.CREATED
    assert request.history == [ProcurementStatus.CREATED]


def test_mark_parsed_transitions_to_parsed():
    request = make_request()
    parsed = ParsedRequest(quantity=5, product_name="Lenovo Laptop", category="Laptop", confidence=0.95)

    request.mark_parsed(parsed)

    assert request.status == ProcurementStatus.PARSED
    assert request.parsed_data == parsed
    assert request.history == [ProcurementStatus.CREATED, ProcurementStatus.PARSED]


def test_cannot_resolve_before_parsing():
    request = make_request()
    with pytest.raises(IllegalStatusTransitionError):
        request.mark_resolved(SKU("LEN-T14-G3"), "SUP-001", Money(Decimal("1200"), "CHF"))


def test_mark_resolved_records_stock_check():
    request = make_request()
    request.mark_parsed(ParsedRequest(5, "Lenovo Laptop", "Laptop", 0.95))

    request.mark_resolved(SKU("LEN-T14-G3"), "SUP-001", Money(Decimal("6000"), "CHF"), stock_check="PASSED")

    assert request.status == ProcurementStatus.RESOLVED
    assert request.stock_check == "PASSED"


def test_mark_validated_only_checks_budget_and_does_not_route_approval():
    """UC-003 (ValidateRequestUseCase) is budget-only; it must NOT decide
    approval routing -- that is UC-004 (CreateOrderUseCase)."""
    request = make_request()
    request.mark_parsed(ParsedRequest(5, "Lenovo Laptop", "Laptop", 0.95))
    request.mark_resolved(SKU("LEN-T14-G3"), "SUP-001", Money(Decimal("6000"), "CHF"))

    request.mark_validated(budget_check="PASSED")

    assert request.status == ProcurementStatus.VALIDATED
    assert request.budget_check == "PASSED"
    assert request.required_approval_levels == []  # not yet decided


def test_submit_for_approval_with_required_levels_goes_to_pending_approval():
    request = make_request()
    request.mark_parsed(ParsedRequest(5, "Lenovo Laptop", "Laptop", 0.95))
    request.mark_resolved(SKU("LEN-T14-G3"), "SUP-001", Money(Decimal("6000"), "CHF"))
    request.mark_validated()

    request.submit_for_approval([ApprovalLevel.MANAGER])

    assert request.status == ProcurementStatus.PENDING_APPROVAL


def test_submit_for_approval_with_no_required_levels_auto_approves():
    request = make_request()
    request.mark_parsed(ParsedRequest(1, "Pen", "Office Supplies", 0.95))
    request.mark_resolved(SKU("PEN-001"), "SUP-001", Money(Decimal("2.00"), "CHF"))
    request.mark_validated()

    request.submit_for_approval([])

    assert request.status == ProcurementStatus.APPROVED


def test_approved_request_cannot_be_rejected():
    """Rule: an APPROVED request cannot be modified/re-approved (rule 4)."""
    request = make_request()
    request.mark_parsed(ParsedRequest(1, "Pen", "Office Supplies", 0.95))
    request.mark_resolved(SKU("PEN-001"), "SUP-001", Money(Decimal("2.00"), "CHF"))
    request.mark_validated()
    request.submit_for_approval([])  # -> APPROVED (auto)

    with pytest.raises(IllegalStatusTransitionError):
        request.reject()


def test_rejected_request_is_terminal():
    request = make_request()
    request.mark_parsed(ParsedRequest(5, "Lenovo Laptop", "Laptop", 0.95))
    request.mark_resolved(SKU("LEN-T14-G3"), "SUP-001", Money(Decimal("6000"), "CHF"))
    request.mark_validated()
    request.submit_for_approval([ApprovalLevel.MANAGER])
    request.reject()

    assert request.status == ProcurementStatus.REJECTED
    with pytest.raises(IllegalStatusTransitionError):
        request.approve()
