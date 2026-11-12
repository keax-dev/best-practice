# Tema: un puerto del negocio permite sustituir adaptadores.
from typing import Protocol


class NotificationPort(Protocol):
    def notify(self, message: str) -> str: ...


class EmailAdapter:
    def notify(self, message: str) -> str:
        return f"Email: {message}"


class ConsoleAdapter:
    def notify(self, message: str) -> str:
        return f"Console: {message}"


def confirm_order(order_id: str, notifier: NotificationPort) -> str:
    return notifier.notify(f"Confirmed {order_id}")


if __name__ == "__main__":
    print(confirm_order("order-1", EmailAdapter()))
    print(confirm_order("order-1", ConsoleAdapter()))
