# Tema: flujo síncrono de creación, validación y actualización.
from dataclasses import replace
from datetime import UTC, datetime
from uuid import uuid4

from api.clients.inventory import InventoryHTTPClient
from api.models.order import Order
from api.repositories.order import OrderRepository


class OrderService:
    def __init__(
        self, repository: OrderRepository, inventory_client: InventoryHTTPClient
    ) -> None:
        self.repository = repository
        self.inventory_client = inventory_client

    def create(self, product_id: int, quantity: int) -> Order:
        order = Order(
            str(uuid4()), product_id, quantity, "CREADO", None, datetime.now(UTC)
        )
        self.repository.save(order)
        status, reason = self.inventory_client.validate(order)
        order = replace(order, status=status, reason=reason)
        self.repository.save(order)
        return order

    def list_all(self) -> list[Order]:
        return self.repository.list_all()

    def get(self, order_id: str) -> Order:
        return self.repository.get(order_id)
