# Tema: una aplicación y un repositorio nuevos para cada prueba.
import pytest
from api import create_app


@pytest.fixture
def app():
    return create_app({"TESTING": True})


@pytest.fixture
def client(app):
    return app.test_client()
