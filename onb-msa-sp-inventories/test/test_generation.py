# Tema: transformar parámetros y cuerpos según el contrato generado de Inventario.
import subprocess
import sys
from pathlib import Path
from uuid import UUID, uuid4

import pytest
from api.generated.interfaces.inventories_api import InventoryAPI
from api.generated.models.deduction import Deduction
from api.generated.models.deduction_input import DeductionInput
from api.generated.models.product import Product

ROOT = Path(__file__).resolve().parents[2]


def test_generated_interface_is_abstract():
    with pytest.raises(TypeError):
        InventoryAPI()


def test_generated_integer_path_binding(app, client, monkeypatch):
    def get_inventory(product_id, x_user_id, x_user_role):
        assert isinstance(product_id, int)
        assert product_id == 1
        return Product(id=product_id, name="Café", stock=0)

    monkeypatch.setattr(
        app.extensions["inventories_api"], "get_inventory", get_inventory
    )
    result = client.get("/api/v1/inventories/1")
    assert result.status_code == 200
    assert result.json["stock"] == 0


def test_generated_deduction_body_uuid_and_response(app, client, monkeypatch):
    identifier = uuid4()

    def deduct_inventory(body, x_user_id, x_user_role):
        assert isinstance(body, DeductionInput)
        assert isinstance(body.order_id, UUID)
        assert body.order_id == identifier
        return Deduction(
            order_id=body.order_id,
            product_id=body.product_id,
            quantity=body.quantity,
            remaining_stock=8,
        )

    monkeypatch.setattr(
        app.extensions["inventories_api"], "deduct_inventory", deduct_inventory
    )
    result = client.post(
        "/api/v1/inventories/deductions",
        json={"order_id": str(identifier), "product_id": 1, "quantity": 2},
    )
    assert result.status_code == 200
    assert result.json["order_id"] == str(identifier)


def test_generated_sources_are_current():
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/generate_apis.py"),
            "--app",
            "inventories",
            "--check",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
