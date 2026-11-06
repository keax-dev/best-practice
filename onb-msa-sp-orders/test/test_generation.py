# Tema: consumir DTO, parámetros e interfaz generados sin cambiar la lógica de negocio.
import subprocess
import sys
from datetime import UTC, datetime, timedelta, timezone
from pathlib import Path
from uuid import UUID, uuid4

import pytest
from api.generated.clients.inventory.client import InventoryClient
from api.generated.interfaces.orders_api import OrdersAPI
from api.generated.models.order import Order, OrderSchema
from api.generated.models.order_input import OrderInput
from marshmallow import ValidationError

ROOT = Path(__file__).resolve().parents[2]


def response(user_id: str, order_id: UUID | None = None) -> Order:
    return Order(
        id=order_id or uuid4(),
        user_id=user_id,
        product_id=1,
        quantity=2,
        status="CONFIRMADO",
        reason=None,
        created_at=datetime.now(UTC),
    )


def test_generated_interface_is_abstract():
    with pytest.raises(TypeError):
        OrdersAPI()


def test_generated_body_and_identity_binding(app, client, monkeypatch):
    def create_order(body, x_user_id, x_user_role):
        assert isinstance(body, OrderInput)
        assert (body.product_id, body.quantity) == (1, 2)
        assert (x_user_id, x_user_role) == ("user-client", "CLIENT")
        return response(x_user_id)

    monkeypatch.setattr(app.extensions["orders_api"], "create_order", create_order)
    result = client.post(
        "/api/v1/orders",
        json={"product_id": 1, "quantity": 2},
        headers={"X-User-Id": "user-client", "X-User-Role": "CLIENT"},
    )
    assert result.status_code == 201
    assert result.json["user_id"] == "user-client"
    assert result.json["created_at"].endswith("Z")
    assert result.json["reason"] is None


def test_generated_uuid_path_binding(app, client, monkeypatch):
    identifier = uuid4()

    def get_order(order_id, x_user_id, x_user_role):
        assert isinstance(order_id, UUID)
        assert order_id == identifier
        return response(x_user_id, order_id)

    monkeypatch.setattr(app.extensions["orders_api"], "get_order", get_order)
    assert client.get(f"/api/v1/orders/{identifier}").json["id"] == str(identifier)


def test_generated_date_time_nullable_and_range_validation():
    model = response("user-client")
    model = Order(
        **{
            **model.__dict__,
            "created_at": datetime(
                2026, 11, 5, 12, tzinfo=timezone(timedelta(hours=2))
            ),
        }
    )
    schema = OrderSchema()
    data = schema.dump(model)
    assert data["created_at"] == "2026-11-05T10:00:00Z"
    restored = schema.load(data)
    assert isinstance(restored.id, UUID)
    assert restored.created_at.utcoffset() == timedelta(0)
    assert restored.reason is None
    for invalid in (True, 0, "2"):
        with pytest.raises(ValidationError):
            schema.load({**data, "quantity": invalid})
    with pytest.raises(ValidationError):
        schema.load({**data, "created_at": "2026-11-05T12:00:00+02:00"})


def test_orders_uses_generated_inventory_client(app):
    assert isinstance(
        app.extensions["order_service"].inventory_client.client, InventoryClient
    )
    assert (
        app.extensions["order_service"].inventory_client.client.base_url
        == "http://127.0.0.1:5000"
    )


def test_generated_sources_are_current():
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/generate_apis.py"),
            "--app",
            "orders",
            "--check",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
