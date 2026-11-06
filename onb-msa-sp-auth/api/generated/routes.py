# Generado desde OpenAPI. No editar; ejecutar scripts/generate_apis.py.
from flask import Blueprint, Flask, request
from flask.typing import ResponseReturnValue
from marshmallow import ValidationError

from api.contract import ContractView
from api.generated.interfaces.auth_api import AuthAPI
from api.generated.models.health import HealthSchema
from api.generated.models.login_input import LoginInputSchema
from api.generated.models.token import TokenSchema


class GetHealthView(ContractView):
    def __init__(self, implementation: AuthAPI) -> None:
        self.implementation = implementation

    def get(self) -> ResponseReturnValue:
        result = self.implementation.get_health()
        try:
            payload = HealthSchema().dump(result)
        except ValidationError as error:
            raise RuntimeError("Invalid generated response serialization") from error
        return payload, 200


class LoginView(ContractView):
    def __init__(self, implementation: AuthAPI) -> None:
        self.implementation = implementation

    def post(self) -> ResponseReturnValue:
        body = LoginInputSchema().load(request.get_json())
        result = self.implementation.login(
            body=body,
        )
        try:
            payload = TokenSchema().dump(result)
        except ValidationError as error:
            raise RuntimeError("Invalid generated response serialization") from error
        return payload, 200


def register_routes(app: Flask, implementation: AuthAPI) -> None:
    blueprint = Blueprint("api_generated", __name__)
    blueprint.add_url_rule(
        "/health".replace("{", "<").replace("}", ">"),
        view_func=GetHealthView.as_view("get_health", implementation),
        methods=["GET"],
    )
    blueprint.add_url_rule(
        "/api/v1/auth/login".replace("{", "<").replace("}", ">"),
        view_func=LoginView.as_view("login", implementation),
        methods=["POST"],
    )
    app.register_blueprint(blueprint)
