# Tema: cada repositorio controla su propio estado.
class OrderRepository:
    def __init__(self) -> None:
        self.orders: list[str] = []

    def add(self, order_id: str) -> None:
        self.orders.append(order_id)

    def list_all(self) -> list[str]:
        return list(self.orders)


if __name__ == "__main__":
    first = OrderRepository()
    first.add("order-1")
    print(first.list_all())
    print(OrderRepository().list_all())
