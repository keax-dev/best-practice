# Tema: flujo síncrono de creación, validación y actualización.
from dataclasses import replace
from datetime import UTC, datetime
from uuid import uuid4

from api.clients.inventory import InventoryHTTPClient
from api.errors import BusinessError
from api.models.order import Order
from api.repositories.order import OrderRepository


class OrderService:
    def __init__(
        self, repository: OrderRepository, inventory_client: InventoryHTTPClient
    ) -> None:
        self.repository = repository
        self.inventory_client = inventory_client

    def create(self, product_id: int, quantity: int, user_id: str) -> Order:
        order = Order(
            str(uuid4()),
            user_id,
            product_id,
            quantity,
            "CREADO",
            None,
            datetime.now(UTC),
        )
        self.repository.save(order)
        status, reason = self.inventory_client.validate(order)
        order = replace(order, status=status, reason=reason)
        self.repository.save(order)
        return order

    def list_all(self, user_id: str, role: str) -> list[Order]:
        orders = self.repository.list_all()
        return (
            orders
            if role == "ADMIN"
            else [order for order in orders if order.user_id == user_id]
        )

    def get(self, order_id: str, user_id: str, role: str) -> Order:
        order = self.repository.get(order_id)
        if role != "ADMIN" and order.user_id != user_id:
            # No revelar al cliente si existe un pedido de otro usuario.
            raise BusinessError("ORDER_NOT_FOUND", "Pedido inexistente", 404)
        return order
