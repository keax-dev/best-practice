# Tema: aislar datos y usar credenciales internas explícitas en las pruebas.
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
    return app


@pytest.fixture
def client(app):
    return app.test_client()
