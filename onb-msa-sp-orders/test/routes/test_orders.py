# Tema: comprobar estados de negocio, fallos técnicos y ausencia de efectos inválidos.
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from threading import Event
from uuid import UUID, uuid4

import pytest
import requests
from api.generated.models.order_input import OrderInputSchema
from api.models.order import Order
from marshmallow import ValidationError


def http_response(status: int, body: dict) -> requests.Response:
    import json

    response = requests.Response()
    response.status_code = status
    response._content = json.dumps(body).encode()
    response.headers["Content-Type"] = "application/json"
    return response


def test_confirm_and_client_uses_gateway(client, monkeypatch, wait_order):
    calls = []

    def post(url, **kwargs):
        calls.append((url, kwargs))
        return http_response(200, {**kwargs["json"], "remaining_stock": 8})

    monkeypatch.setattr(requests, "post", post)
    response = client.post("/api/v1/orders", json={"product_id": 1, "quantity": 2})
    assert response.status_code == 201
    assert response.json["status"] == "CREADO"
    order = wait_order(response.json["id"])
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
def test_cancelled(client, monkeypatch, wait_order, status, code, reason):
    monkeypatch.setattr(
        requests,
        "post",
        lambda *args, **kwargs: http_response(
            status, {"code": code, "message": reason, "details": {}}
        ),
    )
    response = client.post("/api/v1/orders", json={"product_id": 1, "quantity": 2})
    assert response.status_code == 201
    assert response.json["status"] == "CREADO"
    order = wait_order(response.json["id"])
    assert order["status"] == "CANCELADO"
    assert order["reason"] == reason


@pytest.mark.parametrize("failure", [requests.ConnectionError, requests.Timeout])
def test_communication_failure_is_saved(client, monkeypatch, wait_order, failure):
    def post(*args, **kwargs):
        raise failure("simulated")

    monkeypatch.setattr(requests, "post", post)
    response = client.post("/api/v1/orders", json={"product_id": 1, "quantity": 1})
    assert response.status_code == 201
    assert response.json["status"] == "CREADO"
    order = wait_order(response.json["id"])
    assert order["status"] == "ERROR_VALIDACION"
    assert order["reason"] == "No se pudo completar la validación"
    assert client.get("/api/v1/orders").json == [order]


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
        app.extensions["order_service"],
        "list_all",
        lambda *args: [
            Order(str(uuid4()), "user-admin", 1, -1, "CREADO", None, datetime.now(UTC))
        ],
    )
    response = client.get("/api/v1/orders")
    assert response.status_code == 500
    assert response.json["code"] == "INTERNAL_ERROR"
    assert "contrato OpenAPI" in caplog.text


def test_invalid_inventory_response_is_technical(client, monkeypatch, wait_order):
    monkeypatch.setattr(
        requests, "post", lambda *args, **kwargs: http_response(200, {"oops": 1})
    )
    response = client.post("/api/v1/orders", json={"product_id": 1, "quantity": 2})
    assert response.json["status"] == "CREADO"
    assert wait_order(response.json["id"])["status"] == "ERROR_VALIDACION"


def test_independent_instances(app):
    from api import create_app

    other = create_app({"TESTING": True})
    assert (
        app.extensions["order_repository"] is not other.extensions["order_repository"]
    )
    assert (
        app.extensions["validation_executor"]
        is not other.extensions["validation_executor"]
    )
    other.extensions["validation_executor"].shutdown(wait=True)


def test_creation_returns_while_inventory_is_blocked(
    app, client, monkeypatch, wait_order
):
    started, release = Event(), Event()

    def validate(order):
        started.set()
        assert release.wait(timeout=5)
        return "CONFIRMADO", None

    monkeypatch.setattr(
        app.extensions["order_service"].inventory_client, "validate", validate
    )
    with ThreadPoolExecutor(max_workers=1) as caller:
        pending = caller.submit(
            client.post, "/api/v1/orders", json={"product_id": 1, "quantity": 2}
        )
        try:
            response = pending.result(timeout=2)
            assert response.status_code == 201
            assert response.json["status"] == "CREADO"
            assert started.wait(timeout=1)
            assert (
                client.get(f"/api/v1/orders/{response.json['id']}").json
                == response.json
            )
        finally:
            release.set()
    assert wait_order(response.json["id"])["status"] == "CONFIRMADO"


def test_unexpected_worker_failure_is_saved(app, client, monkeypatch, wait_order):
    def validate(order):
        raise RuntimeError("simulated unexpected failure")

    monkeypatch.setattr(
        app.extensions["order_service"].inventory_client, "validate", validate
    )
    response = client.post("/api/v1/orders", json={"product_id": 1, "quantity": 1})
    assert response.json["status"] == "CREADO"
    assert wait_order(response.json["id"])["status"] == "ERROR_VALIDACION"


def test_executor_shutdown_does_not_leave_pending_order(app, client, wait_order):
    app.extensions["validation_executor"].shutdown(wait=True)
    response = client.post("/api/v1/orders", json={"product_id": 1, "quantity": 1})
    assert response.status_code == 201
    assert response.json["status"] == "CREADO"
    assert wait_order(response.json["id"])["status"] == "ERROR_VALIDACION"


def test_worker_limit_keeps_other_orders_pending(monkeypatch):
    from api import create_app

    app = create_app({"TESTING": True, "VALIDATION_WORKERS": 1})
    started, release = Event(), Event()
    calls = []

    def validate(order):
        calls.append(order.id)
        started.set()
        assert release.wait(timeout=5)
        return "CONFIRMADO", None

    monkeypatch.setattr(
        app.extensions["order_service"].inventory_client, "validate", validate
    )
    service = app.extensions["order_service"]
    try:
        first = service.create(1, 1, "user-client")
        assert started.wait(timeout=1)
        second = service.create(1, 1, "user-client")
        assert calls == [first.id]
        assert service.get(second.id, "user-client", "CLIENT").status == "CREADO"
        assert first.status == second.status == "CREADO"
    finally:
        release.set()
        app.extensions["validation_executor"].shutdown(wait=True)
    assert calls == [first.id, second.id]
    assert all(
        order.status == "CONFIRMADO"
        for order in service.list_all("user-client", "CLIENT")
    )


@pytest.mark.parametrize("workers", ["0", "-1", "invalid"])
def test_invalid_worker_configuration(monkeypatch, workers):
    from api import create_app

    monkeypatch.setenv("VALIDATION_WORKERS", workers)
    with pytest.raises(ValueError):
        create_app()
