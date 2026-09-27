from datetime import datetime, timezone

from procurement.domain.entities import Approval, ApprovalDecision, ApprovalLevel
from procurement.infrastructure.repositories.sqlalchemy_approval_repository import (
    SqlAlchemyApprovalRepository,
)


def test_save_and_list_for_request(db_session):
    repository = SqlAlchemyApprovalRepository(db_session)
    approval = Approval(
        id="APR-INT-1",
        procurement_request_id="PR-INT-1",
        approver_id="U-MAN-1",
        level=ApprovalLevel.MANAGER,
        decision=ApprovalDecision.APPROVED,
        decided_at=datetime.now(timezone.utc),
    )

    repository.save(approval)
    results = repository.list_for_request("PR-INT-1")

    assert len(results) == 1
    assert results[0].approver_id == "U-MAN-1"
    assert results[0].decision == ApprovalDecision.APPROVED


def test_list_for_request_only_returns_matching_requests(db_session):
    repository = SqlAlchemyApprovalRepository(db_session)
    repository.save(
        Approval(id="APR-INT-2", procurement_request_id="PR-A", approver_id="U-1", level=ApprovalLevel.MANAGER)
    )
    repository.save(
        Approval(id="APR-INT-3", procurement_request_id="PR-B", approver_id="U-2", level=ApprovalLevel.MANAGER)
    )

    results = repository.list_for_request("PR-A")

    assert len(results) == 1
    assert results[0].id == "APR-INT-2"


def test_list_for_request_returns_empty_for_unknown_request(db_session):
    repository = SqlAlchemyApprovalRepository(db_session)
    assert repository.list_for_request("does-not-exist") == []
