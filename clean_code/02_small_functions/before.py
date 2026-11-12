# Tema: una función mezcla validación, cálculo y construcción del resultado.
def build_receipt(items: list[tuple[str, int, int]]) -> str:
    if not items:
        raise ValueError("The order must contain at least one item")
    total = 0
    lines = ["Receipt"]
    for name, price, quantity in items:
        if price <= 0 or quantity <= 0:
            raise ValueError("Price and quantity must be positive")
        subtotal = price * quantity
        total += subtotal
        lines.append(f"{name}: {subtotal} credits")
    lines.append(f"Total: {total} credits")
    return "\n".join(lines)


def main() -> None:
    items = [("Coffee", 5, 2), ("Tea", 3, 1)]
    print(build_receipt(items))


if __name__ == "__main__":
    main()
