# Tema: organizar un recibo en funciones con un propósito y un nivel de detalle claros.
from dataclasses import dataclass


@dataclass(frozen=True)
class OrderItem:
    name: str
    unit_price: int
    quantity: int


def validate_items(items: list[OrderItem]) -> None:
    if not items:
        raise ValueError("The order must contain at least one item")
    for item in items:
        if item.unit_price <= 0 or item.quantity <= 0:
            raise ValueError("Price and quantity must be positive")


def calculate_subtotal(item: OrderItem) -> int:
    return item.unit_price * item.quantity


def format_receipt(items: list[OrderItem], total: int) -> str:
    lines = ["Receipt"]
    for item in items:
        lines.append(f"{item.name}: {calculate_subtotal(item)} credits")
    lines.append(f"Total: {total} credits")
    return "\n".join(lines)


def build_receipt(items: list[OrderItem]) -> str:
    validate_items(items)
    total = sum(calculate_subtotal(item) for item in items)
    return format_receipt(items, total)


def main() -> None:
    items = [OrderItem("Coffee", 5, 2), OrderItem("Tea", 3, 1)]
    print(build_receipt(items))


if __name__ == "__main__":
    main()
