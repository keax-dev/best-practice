# Generado desde OpenAPI. No editar; ejecutar scripts/generate_apis.py.
from flask import Blueprint, Flask, Response, request
from flask.typing import ResponseReturnValue
from marshmallow import ValidationError, fields, validate

from api.contract import ContractView
from api.generated.interfaces.gateway_api import GatewayAPI
from api.generated.models.deduction import DeductionSchema
from api.generated.models.deduction_input import DeductionInputSchema
from api.generated.models.health import HealthSchema
from api.generated.models.login_input import LoginInputSchema
from api.generated.models.order import OrderSchema
from api.generated.models.order_input import OrderInputSchema
from api.generated.models.product import ProductSchema
from api.generated.models.token import TokenSchema


class CreateOrderView(ContractView):
    def __init__(self, implementation: GatewayAPI) -> None:
        self.implementation = implementation

    def post(self) -> ResponseReturnValue:
        body = OrderInputSchema().load(request.get_json())
        result = self.implementation.create_order(
            body=body,
        )
        if isinstance(result, Response):
            return result
        try:
            payload = OrderSchema().dump(result)
        except ValidationError as error:
            raise RuntimeError("Invalid generated response serialization") from error
        return payload, 201


class DeductInventoryView(ContractView):
    def __init__(self, implementation: GatewayAPI) -> None:
        self.implementation = implementation

    def post(self) -> ResponseReturnValue:
        body = DeductionInputSchema().load(request.get_json())
        result = self.implementation.deduct_inventory(
            body=body,
        )
        if isinstance(result, Response):
            return result
        try:
            payload = DeductionSchema().dump(result)
        except ValidationError as error:
            raise RuntimeError("Invalid generated response serialization") from error
        return payload, 200


class GetHealthView(ContractView):
    def __init__(self, implementation: GatewayAPI) -> None:
        self.implementation = implementation

    def get(self) -> ResponseReturnValue:
        result = self.implementation.get_health()
        if isinstance(result, Response):
            return result
        try:
            payload = HealthSchema().dump(result)
        except ValidationError as error:
            raise RuntimeError("Invalid generated response serialization") from error
        return payload, 200


class GetInventoryView(ContractView):
    def __init__(self, implementation: GatewayAPI) -> None:
        self.implementation = implementation

    def get(self, product_id: str) -> ResponseReturnValue:
        product_id = fields.Integer(
            required=True,
            allow_none=False,
            strict=False,
            validate=[validate.Range(min=1)],
        ).deserialize(product_id)
        result = self.implementation.get_inventory(
            product_id=product_id,
        )
        if isinstance(result, Response):
            return result
        try:
            payload = ProductSchema().dump(result)
        except ValidationError as error:
            raise RuntimeError("Invalid generated response serialization") from error
        return payload, 200


class GetOrderView(ContractView):
    def __init__(self, implementation: GatewayAPI) -> None:
        self.implementation = implementation

    def get(self, order_id: str) -> ResponseReturnValue:
        order_id = fields.UUID(
            required=True, allow_none=False, validate=[]
        ).deserialize(order_id)
        result = self.implementation.get_order(
            order_id=order_id,
        )
        if isinstance(result, Response):
            return result
        try:
            payload = OrderSchema().dump(result)
        except ValidationError as error:
            raise RuntimeError("Invalid generated response serialization") from error
        return payload, 200


class ListInventoriesView(ContractView):
    def __init__(self, implementation: GatewayAPI) -> None:
        self.implementation = implementation

    def get(self) -> ResponseReturnValue:
        result = self.implementation.list_inventories()
        if isinstance(result, Response):
            return result
        try:
            payload = ProductSchema(many=True).dump(result)
        except ValidationError as error:
            raise RuntimeError("Invalid generated response serialization") from error
        return payload, 200


class ListOrdersView(ContractView):
    def __init__(self, implementation: GatewayAPI) -> None:
        self.implementation = implementation

    def get(self) -> ResponseReturnValue:
        result = self.implementation.list_orders()
        if isinstance(result, Response):
            return result
        try:
            payload = OrderSchema(many=True).dump(result)
        except ValidationError as error:
            raise RuntimeError("Invalid generated response serialization") from error
        return payload, 200


class LoginView(ContractView):
    def __init__(self, implementation: GatewayAPI) -> None:
        self.implementation = implementation

    def post(self) -> ResponseReturnValue:
        body = LoginInputSchema().load(request.get_json())
        result = self.implementation.login(
            body=body,
        )
        if isinstance(result, Response):
            return result
        try:
            payload = TokenSchema().dump(result)
        except ValidationError as error:
            raise RuntimeError("Invalid generated response serialization") from error
        return payload, 200


def register_routes(app: Flask, implementation: GatewayAPI) -> None:
    blueprint = Blueprint("api_generated", __name__)
    blueprint.add_url_rule(
        "/api/v1/orders".replace("{", "<").replace("}", ">"),
        view_func=CreateOrderView.as_view("create_order", implementation),
        methods=["POST"],
    )
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
        "/api/v1/orders/{order_id}".replace("{", "<").replace("}", ">"),
        view_func=GetOrderView.as_view("get_order", implementation),
        methods=["GET"],
    )
    blueprint.add_url_rule(
        "/api/v1/inventories".replace("{", "<").replace("}", ">"),
        view_func=ListInventoriesView.as_view("list_inventories", implementation),
        methods=["GET"],
    )
    blueprint.add_url_rule(
        "/api/v1/orders".replace("{", "<").replace("}", ">"),
        view_func=ListOrdersView.as_view("list_orders", implementation),
        methods=["GET"],
    )
    blueprint.add_url_rule(
        "/api/v1/auth/login".replace("{", "<").replace("}", ">"),
        view_func=LoginView.as_view("login", implementation),
        methods=["POST"],
    )
    app.register_blueprint(blueprint)
