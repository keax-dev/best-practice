# Tema: probar descuentos, idempotencia y concurrencia mediante la API.
from concurrent.futures import ThreadPoolExecutor
from uuid import uuid4

import pytest
from api import create_app
from api.schema.inventory import DeductionInputSchema
from marshmallow import ValidationError


def payload(**changes):
    return {"order_id": str(uuid4()), "product_id": 1, "quantity": 2, **changes}


def test_list_and_deduct(client):
    assert [product["stock"] for product in client.get("/api/v1/inventories").json] == [
        10,
        5,
        0,
    ]
    response = client.post("/api/v1/inventories/deductions", json=payload())
    assert response.status_code == 200
    assert response.json["remaining_stock"] == 8
    assert client.get("/api/v1/inventories/1").json["stock"] == 8


def test_idempotency_and_conflict(client):
    body = payload()
    first = client.post("/api/v1/inventories/deductions", json=body)
    assert client.post("/api/v1/inventories/deductions", json=body).json == first.json
    for changes in [{"quantity": 3}, {"product_id": 2}]:
        conflict = client.post(
            "/api/v1/inventories/deductions", json={**body, **changes}
        )
        assert conflict.status_code == 409
        assert conflict.json["code"] == "IDEMPOTENCY_CONFLICT"
    assert client.get("/api/v1/inventories/1").json["stock"] == 8


@pytest.mark.parametrize(
    ("changes", "status", "code"),
    [
        ({"quantity": 11}, 409, "INSUFFICIENT_STOCK"),
        ({"product_id": 3}, 409, "INSUFFICIENT_STOCK"),
        ({"product_id": 999}, 404, "PRODUCT_NOT_FOUND"),
    ],
)
def test_rejection_no_mutation(client, changes, status, code):
    before = client.get("/api/v1/inventories").json
    response = client.post("/api/v1/inventories/deductions", json=payload(**changes))
    assert response.status_code == status
    assert response.json["code"] == code
    assert client.get("/api/v1/inventories").json == before


@pytest.mark.parametrize(
    "changes",
    [
        {"quantity": True},
        {"product_id": False},
        {"quantity": 0},
        {"quantity": -1},
        {"quantity": "1"},
        {"order_id": "bad"},
        {"extra": 1},
    ],
)
def test_invalid_contract_and_schema(client, changes):
    body = payload(**changes)
    with pytest.raises(ValidationError):
        DeductionInputSchema().load(body)
    response = client.post("/api/v1/inventories/deductions", json=body)
    assert response.status_code == 400
    assert client.get("/api/v1/inventories/1").json["stock"] == 10


def test_concurrent_stock_never_negative(app):
    def deduct(_):
        with app.test_client() as client:
            return client.post(
                "/api/v1/inventories/deductions", json=payload(quantity=1)
            ).status_code

    with ThreadPoolExecutor(max_workers=12) as pool:
        statuses = list(pool.map(deduct, range(30)))
    assert statuses.count(200) == 10
    assert statuses.count(409) == 20
    assert app.test_client().get("/api/v1/inventories/1").json["stock"] == 0


def test_concurrent_same_order_deducts_once(app):
    body = payload()

    def deduct(_):
        with app.test_client() as client:
            response = client.post("/api/v1/inventories/deductions", json=body)
            assert response.status_code == 200
            return response.json

    with ThreadPoolExecutor(max_workers=10) as pool:
        results = list(pool.map(deduct, range(20)))
    assert all(result == results[0] for result in results)
    assert app.test_client().get("/api/v1/inventories/1").json["stock"] == 8


def test_instances_and_restart_are_independent(client):
    client.post("/api/v1/inventories/deductions", json=payload())
    other = create_app({"TESTING": True}).test_client()
    assert other.get("/api/v1/inventories/1").json["stock"] == 10


def test_missing_product_and_invalid_path(client):
    assert client.get("/api/v1/inventories/999").json["code"] == "PRODUCT_NOT_FOUND"
    assert client.get("/api/v1/inventories/0").status_code == 400


def test_invalid_response_is_logged_and_controlled(app, client, monkeypatch, caplog):
    monkeypatch.setattr(
        app.extensions["inventory_service"], "list_all", lambda: [object()]
    )
    response = client.get("/api/v1/inventories")
    assert response.status_code == 500
    assert response.json["code"] == "INTERNAL_ERROR"
    assert "contrato OpenAPI" in caplog.text
