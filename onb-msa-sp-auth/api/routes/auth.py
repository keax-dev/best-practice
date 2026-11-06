# Tema: login público que delega la comprobación de credenciales.
from flask import Blueprint, current_app, request
from flask.typing import ResponseReturnValue

from api.contract import ContractView
from api.schema.auth import LoginSchema, TokenSchema

blueprint = Blueprint("auth", __name__)


class LoginAPI(ContractView):
    def post(self) -> ResponseReturnValue:
        data = LoginSchema().load(request.get_json())
        return TokenSchema().dump(current_app.extensions["auth_service"].login(**data))


blueprint.add_url_rule(
    "/api/v1/auth/login", view_func=LoginAPI.as_view("login"), methods=["POST"]
)
