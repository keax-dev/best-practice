# Tema: los valores literales no explican la política de envío que representan.
def shipping_cost(subtotal: int) -> int:
    if subtotal >= 100:
        return 0
    return 5


def main() -> None:
    for subtotal in (80, 100, 150):
        print(f"Subtotal: {subtotal}; shipping: {shipping_cost(subtotal)} credits")


if __name__ == "__main__":
    main()
