# Tema: vistas HTTP que delegan la lógica y el almacenamiento.
from flask import Blueprint, current_app, request
from flask.typing import ResponseReturnValue

from api.contract import ContractView
from api.schema.inventory import DeductionInputSchema, DeductionSchema, ProductSchema

blueprint = Blueprint("inventories", __name__)


class InventoryAPI(ContractView):
    def get(self, product_id: str | None = None) -> ResponseReturnValue:
        service = current_app.extensions["inventory_service"]
        if product_id is not None:
            return ProductSchema().dump(service.get(int(product_id)))
        return ProductSchema(many=True).dump(service.list_all())


class DeductionsAPI(ContractView):
    def post(self) -> ResponseReturnValue:
        data = DeductionInputSchema().load(request.get_json())
        # UUID se normaliza para que distintas representaciones sean idempotentes.
        data["order_id"] = str(data["order_id"])
        result = current_app.extensions["inventory_service"].deduct(**data)
        return DeductionSchema().dump(result)


blueprint.add_url_rule(
    "/api/v1/inventories", view_func=InventoryAPI.as_view("list"), methods=["GET"]
)
blueprint.add_url_rule(
    "/api/v1/inventories/<product_id>",
    view_func=InventoryAPI.as_view("detail"),
    methods=["GET"],
)
blueprint.add_url_rule(
    "/api/v1/inventories/deductions",
    view_func=DeductionsAPI.as_view("deduct"),
    methods=["POST"],
)
