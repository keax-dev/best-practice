# Tema: usar DTO e interfaces generados preservando la respuesta del servicio.
import json
import subprocess
import sys
from pathlib import Path
from uuid import UUID, uuid4

import pytest
from api.generated.interfaces.gateway_api import GatewayAPI
from api.generated.models.order_input import OrderInput
from flask import Response

ROOT = Path(__file__).resolve().parents[2]


def order_data(order_id=None):
    return {
        "id": str(order_id or uuid4()),
        "user_id": "user-admin",
        "product_id": 1,
        "quantity": 2,
        "status": "CONFIRMADO",
        "reason": None,
        "created_at": "2026-11-05T12:00:00Z",
    }


def test_generated_interface_is_abstract():
    with pytest.raises(TypeError):
        GatewayAPI()


def test_generated_gateway_preserves_raw_response(app, client, monkeypatch):
    raw = json.dumps(order_data(), indent=2).encode()

    def create_order(body):
        assert isinstance(body, OrderInput)
        return Response(
            raw,
            status=201,
            headers={"Content-Type": "application/json", "X-Example": "preserved"},
        )

    monkeypatch.setattr(app.extensions["gateway_api"], "create_order", create_order)
    result = client.post("/api/v1/orders", json={"product_id": 1, "quantity": 2})
    assert result.status_code == 201
    assert result.data == raw
    assert result.headers["X-Example"] == "preserved"


def test_generated_gateway_uuid_parameter(app, client, monkeypatch):
    identifier = uuid4()

    def get_order(order_id):
        assert isinstance(order_id, UUID)
        assert order_id == identifier
        return Response(
            json.dumps(order_data(identifier)), content_type="application/json"
        )

    monkeypatch.setattr(app.extensions["gateway_api"], "get_order", get_order)
    assert client.get(f"/api/v1/orders/{identifier}").status_code == 200


def test_generated_sources_are_current():
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/generate_apis.py"),
            "--app",
            "gateway",
            "--check",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
