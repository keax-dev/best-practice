# Tema: rechazar tokens inválidos y evitar suplantación mediante encabezados.
import json
from datetime import UTC, datetime, timedelta

import jwt
import pytest
import requests


def forbid_forward(monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("Unauthorized request reached a service")

    monkeypatch.setattr(requests, "request", forbidden)


def test_missing_token_not_forwarded(app, monkeypatch):
    forbid_forward(monkeypatch)
    response = app.test_client().get(
        "/api/v1/orders",
        headers={
            "X-User-Id": "user-admin",
            "X-User-Role": "ADMIN",
            "X-Internal-Key": "fake",
        },
    )
    assert response.status_code == 401
    assert response.json["code"] == "AUTH_REQUIRED"
    assert response.headers["WWW-Authenticate"] == "Bearer"


@pytest.mark.parametrize(
    ("claims", "code"),
    [
        ({"exp": datetime.now(UTC) - timedelta(seconds=1)}, "TOKEN_EXPIRED"),
        ({"iss": "wrong"}, "INVALID_TOKEN"),
        ({"aud": "wrong"}, "INVALID_TOKEN"),
        ({"role": "SERVICE"}, "INVALID_TOKEN"),
        ({"sub": ""}, "INVALID_TOKEN"),
        ({"sub": "user\r\nInjected: yes"}, "INVALID_TOKEN"),
    ],
)
def test_invalid_claims(app, make_token, monkeypatch, claims, code):
    forbid_forward(monkeypatch)
    response = app.test_client().get(
        "/api/v1/orders", headers={"Authorization": "Bearer " + make_token(**claims)}
    )
    assert response.status_code == 401
    assert response.json["code"] == code


def test_altered_signature_and_wrong_algorithm(app, make_token, monkeypatch):
    forbid_forward(monkeypatch)
    token = make_token()
    parts = token.split(".")
    parts[2] = ("A" if parts[2][0] != "A" else "B") + parts[2][1:]
    for invalid in (
        ".".join(parts),
        jwt.encode({"sub": "user-admin"}, "z" * 40, algorithm="HS256"),
        "garbage",
    ):
        assert (
            app.test_client()
            .get("/api/v1/orders", headers={"Authorization": "Bearer " + invalid})
            .status_code
            == 401
        )


def test_missing_required_claim(app, make_token, keys, monkeypatch):
    forbid_forward(monkeypatch)
    claims = jwt.decode(
        make_token(), keys[1], algorithms=["RS256"], audience="coe-backend"
    )
    for name in ["exp", "sub", "role", "iat", "iss", "aud"]:
        incomplete = {key: value for key, value in claims.items() if key != name}
        token = jwt.encode(incomplete, keys[0], algorithm="RS256")
        assert (
            app.test_client()
            .get("/api/v1/orders", headers={"Authorization": "Bearer " + token})
            .status_code
            == 401
        )


@pytest.mark.parametrize("path", ["/api/v1/inventories", "/api/v1/inventories/1"])
def test_client_forbidden_inventory(app, make_token, monkeypatch, path):
    forbid_forward(monkeypatch)
    response = app.test_client().get(
        path,
        headers={
            "Authorization": "Bearer " + make_token(sub="user-client", role="CLIENT")
        },
    )
    assert response.status_code == 403


def test_gateway_replaces_identity_and_strips_credentials(app, make_token, monkeypatch):
    def send(method, url, **kwargs):
        headers = kwargs["headers"]
        assert headers["X-User-Id"] == "user-client"
        assert headers["X-User-Role"] == "CLIENT"
        assert headers["X-Internal-Key"] == app.config["INTERNAL_API_KEY"]
        assert not any(
            name.lower() in {"authorization", "x-orders-service-key"}
            for name in headers
        )
        response = requests.Response()
        response.status_code = 200
        response._content = b"[]"
        response.headers["Content-Type"] = "application/json"
        return response

    monkeypatch.setattr(requests, "request", send)
    response = app.test_client().get(
        "/api/v1/orders",
        headers={
            "Authorization": "Bearer " + make_token(sub="user-client", role="CLIENT"),
            "X-User-Id": "user-admin",
            "X-User-Role": "ADMIN",
            "X-Internal-Key": "fake",
        },
    )
    assert response.status_code == 200


def test_service_key_only_allows_deduction(app, monkeypatch):
    forbid_forward(monkeypatch)
    client = app.test_client()
    headers = {"X-Orders-Service-Key": app.config["ORDERS_SERVICE_KEY"]}
    for path in ("/api/v1/orders", "/api/v1/inventories"):
        assert client.get(path, headers=headers).status_code == 403
    assert (
        client.post(
            "/api/v1/inventories/deductions",
            json={},
            headers={"X-Orders-Service-Key": "wrong"},
        ).status_code
        == 401
    )


def test_service_deduction_uses_service_identity(app, monkeypatch):
    body = {
        "order_id": "550e8400-e29b-41d4-a716-446655440000",
        "product_id": 1,
        "quantity": 2,
    }

    def send(*args, **kwargs):
        assert kwargs["headers"]["X-User-Id"] == "orders-service"
        assert kwargs["headers"]["X-User-Role"] == "SERVICE"
        response = requests.Response()
        response.status_code = 200
        response._content = json.dumps({**body, "remaining_stock": 8}).encode()
        response.headers["Content-Type"] = "application/json"
        return response

    monkeypatch.setattr(requests, "request", send)
    response = app.test_client().post(
        "/api/v1/inventories/deductions",
        json=body,
        headers={"X-Orders-Service-Key": app.config["ORDERS_SERVICE_KEY"]},
    )
    assert response.status_code == 200
