# Tema: aislar el stock y la idempotencia de cada prueba.
import pytest
from api import create_app


@pytest.fixture
def app():
    return create_app({"TESTING": True})


@pytest.fixture
def client(app):
    return app.test_client()
