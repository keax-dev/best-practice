# Tema: aislar datos y usar credenciales internas explícitas en las pruebas.
import time

import pytest
from api import create_app
from flask.testing import FlaskClient

INTERNAL_KEY = "internal-test-key-" + "x" * 32
SERVICE_KEY = "orders-test-key-" + "y" * 32


class InternalClient(FlaskClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.environ_base.update(
            HTTP_X_INTERNAL_KEY=INTERNAL_KEY,
            HTTP_X_USER_ID="user-admin",
            HTTP_X_USER_ROLE="ADMIN",
        )


@pytest.fixture(autouse=True)
def security_environment(monkeypatch):
    monkeypatch.setenv("INTERNAL_API_KEY", INTERNAL_KEY)
    monkeypatch.setenv("ORDERS_SERVICE_KEY", SERVICE_KEY)


@pytest.fixture
def app():
    app = create_app({"TESTING": True})
    app.test_client_class = InternalClient
    yield app
    # Terminar tareas antes de restaurar los mocks y pasar a la siguiente prueba.
    app.extensions["validation_executor"].shutdown(wait=True)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def wait_order(client):
    def wait(order_id: str, timeout: float = 3) -> dict:
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            response = client.get(f"/api/v1/orders/{order_id}")
            assert response.status_code == 200
            if response.json["status"] != "CREADO":
                return response.json
            time.sleep(0.01)
        pytest.fail(f"Order {order_id} did not finish validation")

    return wait
