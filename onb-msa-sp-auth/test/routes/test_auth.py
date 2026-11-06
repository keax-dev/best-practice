# Tema: comprobar usuarios, contraseñas y contenido verificable del JWT.
import jwt
import pytest
from api.schema.auth import LoginSchema
from api.seed import USERS
from marshmallow import ValidationError
from werkzeug.security import check_password_hash


@pytest.mark.parametrize(
    ("username", "password", "user_id", "role"),
    [
        ("admin", "Admin123!", "user-admin", "ADMIN"),
        ("client", "Client123!", "user-client", "CLIENT"),
    ],
)
def test_login_emits_signed_jwt(client, keys, username, password, user_id, role):
    response = client.post(
        "/api/v1/auth/login", json={"username": username, "password": password}
    )
    assert response.status_code == 200
    assert response.json["token_type"] == "Bearer"
    assert response.json["expires_in"] == 900
    claims = jwt.decode(
        response.json["access_token"],
        keys[1],
        algorithms=["RS256"],
        issuer="coe-auth",
        audience="coe-backend",
        options={"require": ["sub", "exp", "iat", "role"]},
    )
    assert claims["sub"] == user_id
    assert claims["role"] == role
    assert claims["exp"] - claims["iat"] == 900
    assert "password" not in claims


@pytest.mark.parametrize(
    ("username", "password"), [("admin", "wrong"), ("missing", "wrong")]
)
def test_wrong_credentials(client, username, password):
    response = client.post(
        "/api/v1/auth/login", json={"username": username, "password": password}
    )
    assert response.status_code == 401
    assert response.json["code"] == "INVALID_CREDENTIALS"


@pytest.mark.parametrize(
    "body",
    [
        {},
        {"username": "admin"},
        {"username": "", "password": "x"},
        {"username": True, "password": "x"},
        {"username": "admin", "password": "x", "role": "ADMIN"},
        {"username": "a" * 65, "password": "x"},
    ],
)
def test_invalid_input_and_schema(client, body):
    assert client.post("/api/v1/auth/login", json=body).status_code == 400
    with pytest.raises(ValidationError):
        LoginSchema().load(body)


def test_passwords_are_hashes():
    assert len(USERS) == 2
    assert check_password_hash(USERS[0].password_hash, "Admin123!")
    assert check_password_hash(USERS[1].password_hash, "Client123!")


def test_content_errors(client):
    assert (
        client.post(
            "/api/v1/auth/login", data="{", content_type="application/json"
        ).status_code
        == 400
    )
    assert client.post("/api/v1/auth/login", data="{}").status_code == 415


def test_invalid_response_controlled(app, client, monkeypatch, caplog):
    monkeypatch.setattr(app.extensions["auth_service"], "login", lambda **kwargs: {})
    response = client.post(
        "/api/v1/auth/login", json={"username": "admin", "password": "Admin123!"}
    )
    assert response.status_code == 500
    assert response.json["code"] == "INTERNAL_ERROR"
    assert "contrato OpenAPI" in caplog.text
