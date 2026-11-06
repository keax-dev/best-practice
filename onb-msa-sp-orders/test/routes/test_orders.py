# Tema: comprobar estados de negocio, fallos técnicos y ausencia de efectos inválidos.
from datetime import datetime
from uuid import UUID, uuid4

import pytest
import requests
from api.schema.order import OrderInputSchema
from marshmallow import ValidationError


def http_response(status: int, body: dict) -> requests.Response:
    import json

    response = requests.Response()
    response.status_code = status
    response._content = json.dumps(body).encode()
    response.headers["Content-Type"] = "application/json"
    return response


def test_confirm_and_client_uses_gateway(client, monkeypatch):
    calls = []

    def post(url, **kwargs):
        calls.append((url, kwargs))
        return http_response(200, {**kwargs["json"], "remaining_stock": 8})

    monkeypatch.setattr(requests, "post", post)
    response = client.post("/api/v1/orders", json={"product_id": 1, "quantity": 2})
    assert response.status_code == 201
    order = response.json
    assert order["status"] == "CONFIRMADO"
    assert order["user_id"] == "user-admin"
    assert order["reason"] is None
    UUID(order["id"])
    assert datetime.fromisoformat(order["created_at"]).utcoffset().total_seconds() == 0
    assert calls[0][0] == "http://127.0.0.1:5000/api/v1/inventories/deductions"
    assert calls[0][1]["timeout"] == (1, 5)
    assert calls[0][1]["allow_redirects"] is False
    assert "X-Orders-Service-Key" in calls[0][1]["headers"]
    assert "Authorization" not in calls[0][1]["headers"]
    assert client.get(f"/api/v1/orders/{order['id']}").json == order
    assert client.get("/api/v1/orders").json == [order]


@pytest.mark.parametrize(
    ("status", "code", "reason"),
    [
        (409, "INSUFFICIENT_STOCK", "Stock insuficiente"),
        (404, "PRODUCT_NOT_FOUND", "Producto inexistente"),
    ],
)
def test_rejected(client, monkeypatch, status, code, reason):
    monkeypatch.setattr(
        requests,
        "post",
        lambda *args, **kwargs: http_response(
            status, {"code": code, "message": reason, "details": {}}
        ),
    )
    response = client.post("/api/v1/orders", json={"product_id": 1, "quantity": 2})
    assert response.status_code == 201
    assert response.json["status"] == "RECHAZADO"
    assert response.json["reason"] == reason


@pytest.mark.parametrize("failure", [requests.ConnectionError, requests.Timeout])
def test_communication_failure_is_saved(client, monkeypatch, failure):
    def post(*args, **kwargs):
        raise failure("simulated")

    monkeypatch.setattr(requests, "post", post)
    response = client.post("/api/v1/orders", json={"product_id": 1, "quantity": 1})
    assert response.status_code == 201
    assert response.json["status"] == "ERROR_VALIDACION"
    assert response.json["reason"] == "No se pudo completar la validación"
    assert client.get("/api/v1/orders").json == [response.json]


@pytest.mark.parametrize(
    "body",
    [
        {},
        {"product_id": 1},
        {"product_id": 0, "quantity": 2},
        {"product_id": True, "quantity": 2},
        {"product_id": 1, "quantity": False},
        {"product_id": 1, "quantity": 0},
        {"product_id": 1, "quantity": -1},
        {"product_id": 1, "quantity": "2"},
        {"product_id": 1, "quantity": 1.5},
        {"product_id": 1, "quantity": 2, "extra": 1},
        [],
        None,
    ],
)
def test_invalid_has_no_effect(client, monkeypatch, body):
    def forbidden(*args, **kwargs):
        pytest.fail("Invalid input reached the HTTP client")

    monkeypatch.setattr(requests, "post", forbidden)
    response = (
        client.post("/api/v1/orders", json=body)
        if body is not None
        else client.post("/api/v1/orders", data="null", content_type="application/json")
    )
    assert response.status_code == 400
    assert response.json["code"] == "INVALID_INPUT"
    assert client.get("/api/v1/orders").json == []


@pytest.mark.parametrize(
    "body",
    [
        {"product_id": True, "quantity": 2},
        {"product_id": 1, "quantity": False},
        {"product_id": 1, "quantity": "2"},
        {"product_id": 1, "quantity": 0},
    ],
)
def test_marshmallow_agrees(body):
    with pytest.raises(ValidationError):
        OrderInputSchema().load(body)


def test_missing_order_and_bad_uuid(client):
    assert client.get(f"/api/v1/orders/{uuid4()}").json["code"] == "ORDER_NOT_FOUND"
    assert client.get("/api/v1/orders/not-a-uuid").status_code == 400


def test_malformed_and_media_type(client):
    assert (
        client.post(
            "/api/v1/orders", data="{", content_type="application/json"
        ).status_code
        == 400
    )
    assert client.post("/api/v1/orders", data="{}").status_code == 415
    assert client.get("/api/v1/orders").json == []


def test_invalid_response_is_controlled(app, client, monkeypatch, caplog):
    monkeypatch.setattr(
        app.extensions["order_service"], "list_all", lambda *args: [object()]
    )
    response = client.get("/api/v1/orders")
    assert response.status_code == 500
    assert response.json["code"] == "INTERNAL_ERROR"
    assert "contrato OpenAPI" in caplog.text


def test_invalid_inventory_response_is_technical(client, monkeypatch):
    monkeypatch.setattr(
        requests, "post", lambda *args, **kwargs: http_response(200, {"oops": 1})
    )
    response = client.post("/api/v1/orders", json={"product_id": 1, "quantity": 2})
    assert response.json["status"] == "ERROR_VALIDACION"


def test_independent_instances(app):
    from api import create_app

    other = create_app({"TESTING": True})
    assert (
        app.extensions["order_repository"] is not other.extensions["order_repository"]
    )
