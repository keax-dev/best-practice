# Tema: la regla de creación no conoce peticiones ni respuestas HTTP.
from uuid import uuid4

from api.models import Order
from api.repository import OrderRepository


class OrderService:
    def __init__(self, repository: OrderRepository) -> None:
        self.repository = repository

    def create(self, quantity: int) -> Order:
        if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity <= 0:
            raise ValueError("Quantity must be a positive integer")
        order = Order(str(uuid4()), quantity)
        self.repository.add(order)
        return order
