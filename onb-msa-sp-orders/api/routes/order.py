# Tema: separar la interfaz HTTP del flujo del pedido.
from uuid import UUID

from flask import Blueprint, current_app, request
from flask.typing import ResponseReturnValue

from api.contract import ContractView
from api.schema.order import OrderInputSchema, OrderSchema

blueprint = Blueprint("orders", __name__)


class OrdersAPI(ContractView):
    def post(self) -> ResponseReturnValue:
        data = OrderInputSchema().load(request.get_json())
        order = current_app.extensions["order_service"].create(**data)
        return OrderSchema().dump(order), 201

    def get(self, order_id: str | None = None) -> ResponseReturnValue:
        service = current_app.extensions["order_service"]
        if order_id is not None:
            return OrderSchema().dump(service.get(str(UUID(order_id))))
        return OrderSchema(many=True).dump(service.list_all())


blueprint.add_url_rule(
    "/api/v1/orders", view_func=OrdersAPI.as_view("collection"), methods=["GET", "POST"]
)
blueprint.add_url_rule(
    "/api/v1/orders/<order_id>", view_func=OrdersAPI.as_view("detail"), methods=["GET"]
)
