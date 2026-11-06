# Tema: Pedidos solo conoce la dirección HTTP del gateway.
from uuid import UUID

import requests
from marshmallow import ValidationError

from api.generated.clients.inventory.client import InventoryClient
from api.generated.clients.inventory.models.deduction import DeductionSchema
from api.generated.clients.inventory.models.deduction_input import DeductionInput
from api.generated.clients.inventory.models.error import ErrorSchema
from api.models.order import Order


class InventoryHTTPClient:
    def __init__(
        self, gateway_url: str, timeout: tuple[float, float], service_key: str
    ) -> None:
        self.client = InventoryClient(
            gateway_url, timeout, {"X-Orders-Service-Key": service_key}
        )

    def validate(self, order: Order) -> tuple[str, str | None]:
        payload = DeductionInput(
            order_id=UUID(order.id),
            product_id=order.product_id,
            quantity=order.quantity,
        )
        try:
            # Sin reintentos: una respuesta perdida puede ocultar un descuento exitoso.
            response = self.client.deduct_inventory(payload)
            if response.status_code == 200:
                data = DeductionSchema().load(response.json())
                if (str(data.order_id), data.product_id, data.quantity) != (
                    order.id,
                    order.product_id,
                    order.quantity,
                ):
                    raise ValueError("Mismatched deduction")
                return "CONFIRMADO", None
            error = ErrorSchema().load(response.json())
            if response.status_code == 404 and error.code == "PRODUCT_NOT_FOUND":
                return "CANCELADO", "Producto inexistente"
            if response.status_code == 409 and error.code == "INSUFFICIENT_STOCK":
                return "CANCELADO", "Stock insuficiente"
        except (requests.RequestException, ValidationError, ValueError):
            pass
        return "ERROR_VALIDACION", "No se pudo completar la validación"
