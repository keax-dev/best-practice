# Tema: guardar pedidos en memoria sin compartirla con otro servicio.
from threading import Lock

from api.errors import BusinessError
from api.models.order import Order


class OrderRepository:
    def __init__(self) -> None:
        self._orders: dict[str, Order] = {}
        self._lock = Lock()

    def save(self, order: Order) -> None:
        with self._lock:
            self._orders[order.id] = order

    def list_all(self) -> list[Order]:
        with self._lock:
            return list(self._orders.values())

    def get(self, order_id: str) -> Order:
        with self._lock:
            order = self._orders.get(order_id)
            if order is None:
                raise BusinessError(
                    "ORDER_NOT_FOUND", "Pedido inexistente", 404, {"order_id": order_id}
                )
            return order
