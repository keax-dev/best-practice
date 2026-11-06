# Tema: probar el login con una clave nueva sin usar los secretos locales.
import pytest
from api import create_app
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


@pytest.fixture(scope="session")
def keys():
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    private = key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    ).decode()
    return private, key.public_key()


@pytest.fixture
def app(keys):
    return create_app({"TESTING": True, "JWT_PRIVATE_KEY": keys[0]})


@pytest.fixture
def client(app):
    return app.test_client()
