# Tema: emitir tokens de prueba con claves aisladas sin iniciar el login.
from datetime import UTC, datetime, timedelta

import jwt
import pytest
from api import create_app
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

INTERNAL_KEY = "internal-test-key-" + "x" * 32
SERVICE_KEY = "orders-test-key-" + "y" * 32


@pytest.fixture(scope="session")
def keys():
    private = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    return private, private.public_key().public_bytes(
        serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode()


@pytest.fixture
def make_token(keys):
    def issue(**changes):
        now = datetime.now(UTC)
        claims = {
            "sub": "user-admin",
            "role": "ADMIN",
            "iss": "coe-auth",
            "aud": "coe-backend",
            "iat": now,
            "exp": now + timedelta(minutes=15),
            **changes,
        }
        return jwt.encode(claims, keys[0], algorithm="RS256")

    return issue


@pytest.fixture
def app(keys):
    return create_app(
        {
            "TESTING": True,
            "JWT_PUBLIC_KEY": keys[1],
            "INTERNAL_API_KEY": INTERNAL_KEY,
            "ORDERS_SERVICE_KEY": SERVICE_KEY,
        }
    )


@pytest.fixture
def client(app, make_token):
    client = app.test_client()
    client.environ_base["HTTP_AUTHORIZATION"] = "Bearer " + make_token()
    return client
