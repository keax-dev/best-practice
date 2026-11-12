# Tema: el repositorio guarda únicamente el estado de su propia instancia.
from threading import Lock

from api.models import Order


class OrderRepository:
    def __init__(self) -> None:
        self._orders: list[Order] = []
        self._lock = Lock()

    def add(self, order: Order) -> None:
        with self._lock:
            if len(self._orders) >= 100:
                raise OverflowError("Demo order limit reached")
            self._orders.append(order)

    def list_all(self) -> list[Order]:
        with self._lock:
            return list(self._orders)
