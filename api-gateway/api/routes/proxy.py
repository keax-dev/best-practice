# Tema: implementar la interfaz generada preservando las respuestas HTTP del destino.
from uuid import UUID

from flask import Response

from api.clients.proxy import ProxyHTTPClient
from api.generated.interfaces.gateway_api import GatewayAPI
from api.generated.models.deduction_input import DeductionInput
from api.generated.models.health import Health
from api.generated.models.login_input import LoginInput
from api.generated.models.order_input import OrderInput


class GatewayAPIImpl(GatewayAPI):
    def __init__(self, client: ProxyHTTPClient, service_name: str) -> None:
        self.client = client
        self.service_name = service_name

    def create_order(self, body: OrderInput) -> Response:
        return self.client.forward("orders")

    def list_orders(self) -> Response:
        return self.client.forward("orders")

    def get_order(self, order_id: UUID) -> Response:
        return self.client.forward("orders")

    def list_inventories(self) -> Response:
        return self.client.forward("inventories")

    def get_inventory(self, product_id: int) -> Response:
        return self.client.forward("inventories")

    def deduct_inventory(self, body: DeductionInput) -> Response:
        return self.client.forward("inventories")

    def login(self, body: LoginInput) -> Response:
        return self.client.forward("auth")

    def get_health(self) -> Health:
        return Health(status="ok", service=self.service_name)
