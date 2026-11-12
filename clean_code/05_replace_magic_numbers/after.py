# Tema: nombrar los valores que expresan decisiones de negocio.
FREE_SHIPPING_THRESHOLD = 100
STANDARD_SHIPPING_COST = 5


def shipping_cost(subtotal: int) -> int:
    if subtotal >= FREE_SHIPPING_THRESHOLD:
        return 0
    return STANDARD_SHIPPING_COST


def main() -> None:
    # El cero conserva un significado evidente: no hay cargo de envío.
    for subtotal in (80, 100, 150):
        print(f"Subtotal: {subtotal}; shipping: {shipping_cost(subtotal)} credits")


if __name__ == "__main__":
    main()
