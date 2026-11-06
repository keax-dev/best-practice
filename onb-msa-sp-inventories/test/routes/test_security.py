# Tema: bloquear acceso directo y limitar el permiso del servicio Pedidos.
from uuid import uuid4


def test_gateway_key_required(client):
    assert (
        client.get("/api/v1/inventories", headers={"X-Internal-Key": ""}).status_code
        == 401
    )
    assert (
        client.get(
            "/api/v1/inventories", headers={"X-Internal-Key": "wrong"}
        ).status_code
        == 401
    )


def test_client_identity_forbidden(client):
    response = client.get(
        "/api/v1/inventories",
        headers={"X-User-Id": "user-client", "X-User-Role": "CLIENT"},
    )
    assert response.status_code == 403


def test_service_only_deductions(client):
    headers = {"X-User-Id": "orders-service", "X-User-Role": "SERVICE"}
    assert client.get("/api/v1/inventories", headers=headers).status_code == 403
    response = client.post(
        "/api/v1/inventories/deductions",
        json={"order_id": str(uuid4()), "product_id": 1, "quantity": 2},
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json["remaining_stock"] == 8
