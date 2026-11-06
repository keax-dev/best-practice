# Tema: respetar el propietario y rechazar identidad enviada fuera del gateway.
import pytest


def test_direct_access_and_fake_identity_rejected(client):
    response = client.get(
        "/api/v1/orders",
        headers={
            "X-Internal-Key": "",
            "X-User-Id": "user-admin",
            "X-User-Role": "ADMIN",
        },
    )
    assert response.status_code == 401
    assert (
        client.get("/api/v1/orders", headers={"X-Internal-Key": "wrong"}).status_code
        == 401
    )
    assert (
        client.get("/api/v1/orders", headers={"X-User-Role": "SERVICE"}).status_code
        == 403
    )


def test_owner_from_internal_identity_not_body(app, client, monkeypatch):
    monkeypatch.setattr(
        app.extensions["order_service"].inventory_client,
        "validate",
        lambda _: ("CONFIRMADO", None),
    )
    body = {"product_id": 1, "quantity": 1}
    admin_order = client.post("/api/v1/orders", json=body).json
    headers = {"X-User-Id": "user-client", "X-User-Role": "CLIENT"}
    response = client.post("/api/v1/orders", json=body, headers=headers)
    assert response.status_code == 201
    client_order = response.json
    assert client_order["user_id"] == "user-client"
    assert admin_order["user_id"] == "user-admin"
    assert len(client.get("/api/v1/orders").json) == 2
    assert client.get("/api/v1/orders", headers=headers).json == [client_order]
    assert (
        client.get(f"/api/v1/orders/{client_order['id']}", headers=headers).json
        == client_order
    )
    assert (
        client.get(f"/api/v1/orders/{admin_order['id']}", headers=headers).status_code
        == 404
    )
    assert client.get(f"/api/v1/orders/{client_order['id']}").status_code == 200
    assert (
        client.post(
            "/api/v1/orders", json={**body, "user_id": "user-admin"}, headers=headers
        ).status_code
        == 400
    )
    assert len(client.get("/api/v1/orders").json) == 2


@pytest.mark.parametrize("role", ["", "SERVICE", "UNKNOWN"])
def test_invalid_internal_role(client, role):
    assert (
        client.get("/api/v1/orders", headers={"X-User-Role": role}).status_code == 403
    )
