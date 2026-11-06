# Generado desde OpenAPI. No editar; ejecutar scripts/generate_apis.py.
from flask import Blueprint, Flask, request
from flask.typing import ResponseReturnValue
from marshmallow import ValidationError, fields, validate

from api.contract import ContractView
from api.generated.interfaces.orders_api import OrdersAPI
from api.generated.models.health import HealthSchema
from api.generated.models.order import OrderSchema
from api.generated.models.order_input import OrderInputSchema


class CreateOrderView(ContractView):
    def __init__(self, implementation: OrdersAPI) -> None:
        self.implementation = implementation

    def post(self) -> ResponseReturnValue:
        body = OrderInputSchema().load(request.get_json())
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
        result = self.implementation.create_order(
            body=body,
            x_user_id=x_user_id,
            x_user_role=x_user_role,
        )
        try:
            payload = OrderSchema().dump(result)
        except ValidationError as error:
            raise RuntimeError("Invalid generated response serialization") from error
        return payload, 201


class GetHealthView(ContractView):
    def __init__(self, implementation: OrdersAPI) -> None:
        self.implementation = implementation

    def get(self) -> ResponseReturnValue:
        result = self.implementation.get_health()
        try:
            payload = HealthSchema().dump(result)
        except ValidationError as error:
            raise RuntimeError("Invalid generated response serialization") from error
        return payload, 200


class GetOrderView(ContractView):
    def __init__(self, implementation: OrdersAPI) -> None:
        self.implementation = implementation

    def get(self, order_id: str) -> ResponseReturnValue:
        order_id = fields.UUID(
            required=True, allow_none=False, validate=[]
        ).deserialize(order_id)
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
        result = self.implementation.get_order(
            order_id=order_id,
            x_user_id=x_user_id,
            x_user_role=x_user_role,
        )
        try:
            payload = OrderSchema().dump(result)
        except ValidationError as error:
            raise RuntimeError("Invalid generated response serialization") from error
        return payload, 200


class ListOrdersView(ContractView):
    def __init__(self, implementation: OrdersAPI) -> None:
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
        result = self.implementation.list_orders(
            x_user_id=x_user_id,
            x_user_role=x_user_role,
        )
        try:
            payload = OrderSchema(many=True).dump(result)
        except ValidationError as error:
            raise RuntimeError("Invalid generated response serialization") from error
        return payload, 200


def register_routes(app: Flask, implementation: OrdersAPI) -> None:
    blueprint = Blueprint("api_generated", __name__)
    blueprint.add_url_rule(
        "/api/v1/orders".replace("{", "<").replace("}", ">"),
        view_func=CreateOrderView.as_view("create_order", implementation),
        methods=["POST"],
    )
    blueprint.add_url_rule(
        "/health".replace("{", "<").replace("}", ">"),
        view_func=GetHealthView.as_view("get_health", implementation),
        methods=["GET"],
    )
    blueprint.add_url_rule(
        "/api/v1/orders/{order_id}".replace("{", "<").replace("}", ">"),
        view_func=GetOrderView.as_view("get_order", implementation),
        methods=["GET"],
    )
    blueprint.add_url_rule(
        "/api/v1/orders".replace("{", "<").replace("}", ">"),
        view_func=ListOrdersView.as_view("list_orders", implementation),
        methods=["GET"],
    )
    app.register_blueprint(blueprint)
