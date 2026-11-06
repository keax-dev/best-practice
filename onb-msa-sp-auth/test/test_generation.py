# Tema: consumir DTO generados y demostrar regeneración sin perder la implementación.
import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml
from api.generated.interfaces.auth_api import AuthAPI
from api.generated.models.login_input import LoginInput, LoginInputSchema
from api.generated.models.token import Token, TokenSchema
from marshmallow import ValidationError

AUTH = Path(__file__).resolve().parents[1]
ROOT = AUTH.parent
SCRIPT = ROOT / "scripts/generate_auth.py"


def generate(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        check=False,
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def test_http_uses_generated_request_and_response(app, client, monkeypatch):
    def login(body: LoginInput) -> Token:
        assert isinstance(body, LoginInput)
        assert body.username == "client"
        return Token(access_token="test-token", token_type="Bearer", expires_in=60)

    monkeypatch.setattr(app.extensions["auth_api"], "login", login)
    response = client.post(
        "/api/v1/auth/login", json={"username": "client", "password": "Client123!"}
    )
    assert response.status_code == 200
    assert response.json == {
        "access_token": "test-token",
        "token_type": "Bearer",
        "expires_in": 60,
    }


def test_generated_interface_requires_implementation():
    with pytest.raises(TypeError):
        AuthAPI()

    class MissingLogin(AuthAPI):
        def get_health(self):
            return None

    with pytest.raises(TypeError):
        MissingLogin()


def test_generated_models_round_trip_and_validate():
    data = {"username": "client", "password": "Client123!"}
    model = LoginInputSchema().load(data)
    assert isinstance(model, LoginInput)
    assert LoginInputSchema().dump(model) == data
    token = TokenSchema().load(
        {"access_token": "token", "token_type": "Bearer", "expires_in": 1}
    )
    assert isinstance(token, Token)
    for invalid in (0, True, "10"):
        with pytest.raises(ValidationError):
            TokenSchema().load(
                {"access_token": "token", "token_type": "Bearer", "expires_in": invalid}
            )


def test_generated_files_are_current():
    result = generate("--check")
    assert result.returncode == 0, result.stdout + result.stderr


def test_regenerate_from_changed_contract_preserves_manual_implementation(tmp_path):
    manual = AUTH / "api/routes/auth.py"
    original = manual.read_bytes()
    document = yaml.safe_load(
        (AUTH / "contracts/openapi.yaml").read_text(encoding="utf-8")
    )
    document["components"]["schemas"]["LoginInput"]["properties"]["username"][
        "maxLength"
    ] = 3
    document["paths"]["/api/v1/auth/login"]["post"]["operationId"] = "signIn"
    document["paths"]["/api/v1/auth/login"]["post"]["requestBody"]["content"][
        "application/json"
    ]["example"]["username"] = "abc"
    contract = tmp_path / "openapi.yaml"
    contract.write_text(yaml.safe_dump(document), encoding="utf-8")
    output = tmp_path / "generated"
    result = generate("--contract", str(contract), "--output", str(output))
    assert result.returncode == 0, result.stdout + result.stderr
    specification = importlib.util.spec_from_file_location(
        "generated_login_test", output / "models/login_input.py"
    )
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    try:
        specification.loader.exec_module(module)
        assert (
            module.LoginInputSchema()
            .load({"username": "abc", "password": "secret"})
            .username
            == "abc"
        )
        with pytest.raises(ValidationError):
            module.LoginInputSchema().load({"username": "abcd", "password": "secret"})
    finally:
        del sys.modules[specification.name]
    assert "def sign_in(" in (output / "interfaces/auth_api.py").read_text()
    generated_routes = (output / "routes.py").read_text()
    assert "self.implementation.sign_in(" in generated_routes
    assert "body=body," in generated_routes
    snapshot = {
        path.relative_to(output): path.read_bytes()
        for path in output.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    }
    result = generate("--contract", str(contract), "--output", str(output))
    assert result.returncode == 0, result.stdout + result.stderr
    assert {path: (output / path).read_bytes() for path in snapshot} == snapshot
    assert manual.read_bytes() == original


def test_check_detects_modified_generated_file_without_overwriting(tmp_path):
    output = tmp_path / "generated"
    shutil.copytree(
        AUTH / "api/generated", output, ignore=shutil.ignore_patterns("__pycache__")
    )
    path = output / "models/token.py"
    path.write_bytes(path.read_text(encoding="utf-8").replace("\n", "\r\n").encode())
    normalized = generate("--check", "--output", str(output))
    assert normalized.returncode == 0, normalized.stdout + normalized.stderr
    changed = path.read_bytes() + b"\n# Cambio de prueba.\n"
    path.write_bytes(changed)
    result = generate("--check", "--output", str(output))
    assert result.returncode == 1
    assert "models/token.py" in result.stdout
    assert path.read_bytes() == changed
