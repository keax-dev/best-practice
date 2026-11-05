# Tema: verificar el transporte HTTP y los errores del gateway.
import json
from uuid import uuid4

import pytest
import requests
from api.clients.proxy import clean_headers


def upstream(body, status=200, headers=None):
    response = requests.Response()
    response.status_code = status
    response._content = json.dumps(body).encode()
    response.headers.update({"Content-Type": "application/json", **(headers or {})})
    return response


def test_forward_preserves_query_headers_and_response(client, monkeypatch):
    calls = []
    body = [{"id": 1, "name": "Café", "stock": 10}]

    def send(*args, **kwargs):
        calls.append((args, kwargs))
        return upstream(
            body,
            headers={
                "X-Example": "value",
                "Connection": "X-Private",
                "X-Private": "hidden",
            },
        )

    monkeypatch.setattr(requests, "request", send)
    response = client.get(
        "/api/v1/inventories?tag=a&tag=b", headers={"X-Request-ID": "abc"}
    )
    assert response.status_code == 200
    assert response.json == body
    assert response.headers["X-Example"] == "value"
    assert "X-Private" not in response.headers
    args, kwargs = calls[0]
    assert args == ("GET", "http://127.0.0.1:5002/api/v1/inventories")
    assert kwargs["params"] == [("tag", "a"), ("tag", "b")]
    assert kwargs["headers"]["X-Request-Id"] == "abc"
    assert "Host" not in kwargs["headers"]
    assert kwargs["timeout"] == (1, 2)


def test_post_preserves_body_and_business_error(client, monkeypatch):
    body = {"order_id": str(uuid4()), "product_id": 1, "quantity": 20}
    error = {
        "code": "INSUFFICIENT_STOCK",
        "message": "Stock insuficiente",
        "details": {"product_id": 1},
    }

    def send(method, url, **kwargs):
        assert method == "POST"
        assert url.endswith("/api/v1/inventories/deductions")
        assert json.loads(kwargs["data"]) == body
        return upstream(error, 409)

    monkeypatch.setattr(requests, "request", send)
    response = client.post("/api/v1/inventories/deductions", json=body)
    assert response.status_code == 409
    assert response.json == error


@pytest.mark.parametrize(
    ("failure", "status", "code"),
    [
        (requests.ConnectionError, 502, "SERVICE_UNAVAILABLE"),
        (requests.Timeout, 504, "UPSTREAM_TIMEOUT"),
    ],
)
def test_transport_errors(client, monkeypatch, failure, status, code):
    def send(*args, **kwargs):
        raise failure("secret technical information")

    monkeypatch.setattr(requests, "request", send)
    response = client.get("/api/v1/inventories")
    assert response.status_code == status
    assert response.json["code"] == code
    assert "secret" not in response.text


@pytest.mark.parametrize(
    ("body", "status"),
    [
        ({"wrong": True}, 200),
        ([{"id": 1, "name": "Café", "stock": -1}], 200),
        ({"message": "missing code"}, 500),
        ({}, 302),
    ],
)
def test_invalid_upstream_response_becomes_502(
    client, monkeypatch, caplog, body, status
):
    monkeypatch.setattr(
        requests, "request", lambda *args, **kwargs: upstream(body, status)
    )
    response = client.get("/api/v1/inventories")
    assert response.status_code == 502
    assert response.json["code"] == "INVALID_RESPONSE"
    assert "contrato OpenAPI" in caplog.text


def test_invalid_input_not_forwarded(client, monkeypatch):
    def send(*args, **kwargs):
        pytest.fail("Invalid request was forwarded")

    monkeypatch.setattr(requests, "request", send)
    assert (
        client.post(
            "/api/v1/orders", json={"product_id": True, "quantity": 1}
        ).status_code
        == 400
    )
    assert (
        client.post(
            "/api/v1/orders", data="{", content_type="application/json"
        ).status_code
        == 400
    )
    assert client.post("/api/v1/orders", data="{}").status_code == 415
    assert client.get("/api/v1/unknown").status_code == 404
    assert client.delete("/api/v1/orders").status_code == 405


def test_local_health_and_docs_do_not_call_services(client, monkeypatch):
    def send(*args, **kwargs):
        pytest.fail("Local resource called a service")

    monkeypatch.setattr(requests, "request", send)
    assert client.get("/health").json == {"status": "ok", "service": "api-gateway"}
    assert client.get("/openapi.yaml").status_code == 200
    assert "/openapi.yaml" in client.get("/docs").text


def test_loop_blocked(client, monkeypatch):
    def send(*args, **kwargs):
        pytest.fail("Loop reached the destination")

    monkeypatch.setattr(requests, "request", send)
    response = client.get(
        "/api/v1/inventories", headers={"X-Gateway-Route": "inventories"}
    )
    assert response.status_code == 502


def test_dynamic_connection_headers_removed():
    headers = clean_headers(
        {
            "Connection": "X-Private",
            "X-Private": "secret",
            "Content-Length": "100",
            "Content-Type": "application/json",
        }
    )
    assert headers == {"Content-Type": "application/json"}
