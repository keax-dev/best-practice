# Generado desde OpenAPI. No editar; ejecutar scripts/generate_apis.py.
from flask import Blueprint, Flask, request
from flask.typing import ResponseReturnValue
from marshmallow import ValidationError, fields, validate

from api.contract import ContractView
from api.generated.interfaces.inventories_api import InventoryAPI
from api.generated.models.deduction import DeductionSchema
from api.generated.models.deduction_input import DeductionInputSchema
from api.generated.models.health import HealthSchema
from api.generated.models.product import ProductSchema


class DeductInventoryView(ContractView):
    def __init__(self, implementation: InventoryAPI) -> None:
        self.implementation = implementation

    def post(self) -> ResponseReturnValue:
        body = DeductionInputSchema().load(request.get_json())
        x_user_id = fields.String(
            required=True,
            allow_none=False,
            validate=[validate.Regexp("^[a-zA-Z0-9_-]{1,64}$")],
        ).deserialize(request.headers.get("X-User-Id"))
        x_user_role = fields.String(
            required=True,
            allow_none=False,
            validate=[validate.OneOf(["ADMIN", "CLIENT", "SERVICE"])],
        ).deserialize(request.headers.get("X-User-Role"))
        result = self.implementation.deduct_inventory(
            body=body,
            x_user_id=x_user_id,
            x_user_role=x_user_role,
        )
        try:
            payload = DeductionSchema().dump(result)
        except ValidationError as error:
            raise RuntimeError("Invalid generated response serialization") from error
        return payload, 200


class GetHealthView(ContractView):
    def __init__(self, implementation: InventoryAPI) -> None:
        self.implementation = implementation

    def get(self) -> ResponseReturnValue:
        result = self.implementation.get_health()
        try:
            payload = HealthSchema().dump(result)
        except ValidationError as error:
            raise RuntimeError("Invalid generated response serialization") from error
        return payload, 200


class GetInventoryView(ContractView):
    def __init__(self, implementation: InventoryAPI) -> None:
        self.implementation = implementation

    def get(self, product_id: str) -> ResponseReturnValue:
        product_id = fields.Integer(
            required=True,
            allow_none=False,
            strict=False,
            validate=[validate.Range(min=1)],
        ).deserialize(product_id)
        x_user_id = fields.String(
            required=True,
            allow_none=False,
            validate=[validate.Regexp("^[a-zA-Z0-9_-]{1,64}$")],
        ).deserialize(request.headers.get("X-User-Id"))
        x_user_role = fields.String(
            required=True,
            allow_none=False,
            validate=[validate.OneOf(["ADMIN", "CLIENT", "SERVICE"])],
        ).deserialize(request.headers.get("X-User-Role"))
        result = self.implementation.get_inventory(
            product_id=product_id,
            x_user_id=x_user_id,
            x_user_role=x_user_role,
        )
        try:
            payload = ProductSchema().dump(result)
        except ValidationError as error:
            raise RuntimeError("Invalid generated response serialization") from error
        return payload, 200


class ListInventoriesView(ContractView):
    def __init__(self, implementation: InventoryAPI) -> None:
        self.implementation = implementation

    def get(self) -> ResponseReturnValue:
        x_user_id = fields.String(
            required=True,
            allow_none=False,
            validate=[validate.Regexp("^[a-zA-Z0-9_-]{1,64}$")],
        ).deserialize(request.headers.get("X-User-Id"))
        x_user_role = fields.String(
            required=True,
            allow_none=False,
            validate=[validate.OneOf(["ADMIN", "CLIENT", "SERVICE"])],
        ).deserialize(request.headers.get("X-User-Role"))
        result = self.implementation.list_inventories(
            x_user_id=x_user_id,
            x_user_role=x_user_role,
        )
        try:
            payload = ProductSchema(many=True).dump(result)
        except ValidationError as error:
            raise RuntimeError("Invalid generated response serialization") from error
        return payload, 200


def register_routes(app: Flask, implementation: InventoryAPI) -> None:
    blueprint = Blueprint("api_generated", __name__)
    blueprint.add_url_rule(
        "/api/v1/inventories/deductions".replace("{", "<").replace("}", ">"),
        view_func=DeductInventoryView.as_view("deduct_inventory", implementation),
        methods=["POST"],
    )
    blueprint.add_url_rule(
        "/health".replace("{", "<").replace("}", ">"),
        view_func=GetHealthView.as_view("get_health", implementation),
        methods=["GET"],
    )
    blueprint.add_url_rule(
        "/api/v1/inventories/{product_id}".replace("{", "<").replace("}", ">"),
        view_func=GetInventoryView.as_view("get_inventory", implementation),
        methods=["GET"],
    )
    blueprint.add_url_rule(
        "/api/v1/inventories".replace("{", "<").replace("}", ">"),
        view_func=ListInventoriesView.as_view("list_inventories", implementation),
        methods=["GET"],
    )
    app.register_blueprint(blueprint)
