"""End-to-end tests: the direct catalog-selection intake mode, and domain
errors surfacing as HTTP 422 responses."""


def test_catalog_selection_resolves_directly(client):
    res = client.post(
        "/procurement-requests/from-catalog",
        json={"requester_id": "U-REQ-1", "cost_center_id": "CC-IT", "sku": "LEN-T14-G3", "quantity": 2},
    )
    assert res.status_code == 201
    body = res.json()
    assert body["status"] == "RESOLVED"
    assert body["amount"] == "2400.00"
    assert body["stock_check"] == "PASSED"


def test_catalog_selection_with_unknown_sku_returns_422(client):
    res = client.post(
        "/procurement-requests/from-catalog",
        json={"requester_id": "U-REQ-1", "cost_center_id": "CC-IT", "sku": "NOT-A-REAL-SKU", "quantity": 1},
    )
    assert res.status_code == 422


def test_catalog_selection_from_unapproved_supplier_returns_422(client):
    # HP-X360 in the seed data is supplied by SUP-002, which is unapproved.
    res = client.post(
        "/procurement-requests/from-catalog",
        json={"requester_id": "U-REQ-1", "cost_center_id": "CC-IT", "sku": "HP-X360", "quantity": 1},
    )
    assert res.status_code == 422


def test_approving_with_wrong_role_returns_422(client):
    create_res = client.post(
        "/procurement-requests/from-catalog",
        json={"requester_id": "U-REQ-1", "cost_center_id": "CC-IT", "sku": "LEN-T14-G3", "quantity": 5},
    )
    request_id = create_res.json()["request_id"]
    client.post(f"/procurement-requests/{request_id}/validate")
    client.post(f"/procurement-requests/{request_id}/create-order")

    # U-REQ-1 is a REQUESTER, not a MANAGER -- must not be allowed to approve.
    res = client.post(
        f"/procurement-requests/{request_id}/approvals",
        json={"approver_id": "U-REQ-1", "level": "MANAGER", "decision": "APPROVED"},
    )
    assert res.status_code == 422
