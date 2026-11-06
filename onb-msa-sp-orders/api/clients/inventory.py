# Tema: Pedidos solo conoce la dirección HTTP del gateway.
import requests
from marshmallow import ValidationError

from api.models.order import Order
from api.schema.order import DeductionSchema, ErrorSchema


class InventoryHTTPClient:
    def __init__(
        self, gateway_url: str, timeout: tuple[float, float], service_key: str
    ) -> None:
        self.url = gateway_url.rstrip("/") + "/api/v1/inventories/deductions"
        self.timeout = timeout
        self.service_key = service_key

    def validate(self, order: Order) -> tuple[str, str | None]:
        payload = {
            "order_id": order.id,
            "product_id": order.product_id,
            "quantity": order.quantity,
        }
        try:
            # Sin reintentos: una respuesta perdida puede ocultar un descuento exitoso.
            response = requests.post(
                self.url,
                json=payload,
                timeout=self.timeout,
                allow_redirects=False,
                headers={"X-Orders-Service-Key": self.service_key},
            )
            if response.status_code == 200:
                data = DeductionSchema().load(response.json())
                if (str(data["order_id"]), data["product_id"], data["quantity"]) != (
                    order.id,
                    order.product_id,
                    order.quantity,
                ):
                    raise ValueError("Mismatched deduction")
                return "CONFIRMADO", None
            error = ErrorSchema().load(response.json())
            if response.status_code == 404 and error["code"] == "PRODUCT_NOT_FOUND":
                return "RECHAZADO", "Producto inexistente"
            if response.status_code == 409 and error["code"] == "INSUFFICIENT_STOCK":
                return "RECHAZADO", "Stock insuficiente"
        except (requests.RequestException, ValidationError, ValueError):
            pass
        return "ERROR_VALIDACION", "No se pudo completar la validación"
