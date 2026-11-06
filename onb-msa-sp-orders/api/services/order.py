# Tema: crear pedidos y validar inventario en segundo plano.
import logging
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from datetime import UTC, datetime
from uuid import uuid4

from api.clients.inventory import InventoryHTTPClient
from api.errors import BusinessError
from api.models.order import Order
from api.repositories.order import OrderRepository

logger = logging.getLogger(__name__)


class OrderService:
    def __init__(
        self,
        repository: OrderRepository,
        inventory_client: InventoryHTTPClient,
        executor: ThreadPoolExecutor,
    ) -> None:
        self.repository = repository
        self.inventory_client = inventory_client
        self.executor = executor

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
        try:
            self.executor.submit(self._validate, order)
        except RuntimeError:
            # Si el ejecutor se está cerrando, el pedido conserva un resultado consultable.
            logger.exception(
                "No se pudo programar la validación del pedido %s", order.id
            )
            self.repository.save(
                replace(
                    order,
                    status="ERROR_VALIDACION",
                    reason="No se pudo completar la validación",
                )
            )
        # El objeto es inmutable: la respuesta siempre conserva el estado inicial.
        return order

    def _validate(self, order: Order) -> None:
        try:
            status, reason = self.inventory_client.validate(order)
        except Exception:
            # Un error inesperado del trabajador tampoco debe dejar el pedido en CREADO.
            logger.exception("Falló la validación del pedido %s", order.id)
            status, reason = "ERROR_VALIDACION", "No se pudo completar la validación"
        self.repository.save(replace(order, status=status, reason=reason))

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
