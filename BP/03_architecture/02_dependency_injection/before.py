# Tema: el servicio construye el repositorio concreto.
class MemoryRepository:
    def find(self, order_id: str) -> str:
        return f"Memory: {order_id}"

class OrderService:
    def __init__(self) -> None:
        self.repository = MemoryRepository()

    def get(self, order_id: str) -> str:
        return self.repository.find(order_id)

if __name__ == "__main__":
    print(OrderService().get("order-1"))
