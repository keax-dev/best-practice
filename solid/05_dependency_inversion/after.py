# Tema: depender de un contrato e inyectar la implementación desde el exterior.
from typing import Protocol


class MessageSender(Protocol):
    def send(self, message: str) -> None: ...


class EmailSender:
    def send(self, message: str) -> None:
        print(f"Email: {message}")


class SmsSender:
    def send(self, message: str) -> None:
        print(f"SMS: {message}")


class OrderService:
    def __init__(self, sender: MessageSender) -> None:
        self.sender = sender

    def confirm(self, order_id: str) -> None:
        self.sender.send(f"Order {order_id} confirmed")


def main() -> None:
    # La composición selecciona el canal; el servicio conserva su regla de negocio.
    OrderService(EmailSender()).confirm("order-1")
    OrderService(SmsSender()).confirm("order-2")


if __name__ == "__main__":
    main()
