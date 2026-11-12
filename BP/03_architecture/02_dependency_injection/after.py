# Tema: el servicio declara lo que necesita y la composición elige la herramienta.
from typing import Protocol


class OrderRepository(Protocol):
    def find(self, order_id: str) -> str: ...


class MemoryRepository:
    def find(self, order_id: str) -> str:
        return f"Memory: {order_id}"


class OrderService:
    def __init__(self, repository: OrderRepository) -> None:
        self.repository = repository

    def get(self, order_id: str) -> str:
        return self.repository.find(order_id)


if __name__ == "__main__":
    print(OrderService(MemoryRepository()).get("order-1"))
