# Tema: el servicio construye una dependencia concreta y queda acoplado al correo.
class EmailSender:
    def send(self, message: str) -> None:
        print(f"Email: {message}")


class OrderService:
    def __init__(self) -> None:
        self.sender = EmailSender()

    def confirm(self, order_id: str) -> None:
        self.sender.send(f"Order {order_id} confirmed")


def main() -> None:
    OrderService().confirm("order-1")


if __name__ == "__main__":
    main()
