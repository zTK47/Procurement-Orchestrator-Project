"""End-to-end test: drives the full free-text intake pipeline through real
HTTP calls against the FastAPI app (seeded data from infrastructure/seed_data.py,
same as demo.py's Scenario A)."""


def test_full_pipeline_from_text_to_approved(client):
    create_res = client.post(
        "/procurement-requests",
        json={
            "requester_id": "U-REQ-1",
            "cost_center_id": "CC-IT",
            "raw_text": "I need 5 new Lenovo Laptops for the IT department",
        },
    )
    assert create_res.status_code == 201
    body = create_res.json()
    assert body["status"] == "PARSED"
    request_id = body["request_id"]

    resolve_res = client.post(f"/procurement-requests/{request_id}/resolve")
    assert resolve_res.status_code == 200
    assert resolve_res.json()["status"] == "RESOLVED"
    assert resolve_res.json()["resolved_sku"] == "LEN-T14-G3"

    validate_res = client.post(f"/procurement-requests/{request_id}/validate")
    assert validate_res.status_code == 200
    assert validate_res.json()["status"] == "VALIDATED"
    assert validate_res.json()["budget_check"] == "PASSED"

    order_res = client.post(f"/procurement-requests/{request_id}/create-order")
    assert order_res.status_code == 200
    assert order_res.json()["status"] == "PENDING_APPROVAL"
    assert order_res.json()["required_approval_levels"] == ["MANAGER"]

    approval_res = client.post(
        f"/procurement-requests/{request_id}/approvals",
        json={"approver_id": "U-MAN-1", "level": "MANAGER", "decision": "APPROVED"},
    )
    assert approval_res.status_code == 200
    assert approval_res.json()["status"] == "APPROVED"

    get_res = client.get(f"/procurement-requests/{request_id}")
    assert get_res.status_code == 200
    assert get_res.json()["status"] == "APPROVED"
    assert get_res.json()["history"] == [
        "CREATED", "PARSED", "RESOLVED", "VALIDATED", "PENDING_APPROVAL", "APPROVED",
    ]


def test_get_unknown_request_returns_404(client):
    res = client.get("/procurement-requests/does-not-exist")
    assert res.status_code == 404


def test_health_endpoint(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


def test_frontend_is_served_at_root(client):
    res = client.get("/")
    assert res.status_code == 200
    assert "Procurement Orchestrator" in res.text
