# Tema: publicar exclusivamente las operaciones del contrato.
from flask import Blueprint, current_app
from flask.typing import ResponseReturnValue

from api.contract import ContractView

blueprint = Blueprint("gateway", __name__)


class OrdersAPI(ContractView):
    def get(self, order_id: str | None = None) -> ResponseReturnValue:
        return current_app.extensions["proxy_client"].forward("orders")

    def post(self) -> ResponseReturnValue:
        return current_app.extensions["proxy_client"].forward("orders")


class InventoryAPI(ContractView):
    def get(self, product_id: str | None = None) -> ResponseReturnValue:
        return current_app.extensions["proxy_client"].forward("inventories")


class DeductionsAPI(ContractView):
    def post(self) -> ResponseReturnValue:
        return current_app.extensions["proxy_client"].forward("inventories")


blueprint.add_url_rule(
    "/api/v1/orders", view_func=OrdersAPI.as_view("orders"), methods=["GET", "POST"]
)
blueprint.add_url_rule(
    "/api/v1/orders/<order_id>", view_func=OrdersAPI.as_view("order"), methods=["GET"]
)
blueprint.add_url_rule(
    "/api/v1/inventories",
    view_func=InventoryAPI.as_view("inventories"),
    methods=["GET"],
)
blueprint.add_url_rule(
    "/api/v1/inventories/<product_id>",
    view_func=InventoryAPI.as_view("inventory"),
    methods=["GET"],
)
blueprint.add_url_rule(
    "/api/v1/inventories/deductions",
    view_func=DeductionsAPI.as_view("deductions"),
    methods=["POST"],
)
