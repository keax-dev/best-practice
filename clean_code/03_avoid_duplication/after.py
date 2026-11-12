# Tema: conservar una sola definición de una regla compartida por dos canales.
DISCOUNT_THRESHOLD = 100
DISCOUNT_AMOUNT = 10


def apply_discount(subtotal: int) -> int:
    if subtotal >= DISCOUNT_THRESHOLD:
        return subtotal - DISCOUNT_AMOUNT
    return subtotal


def calculate_online_total(subtotal: int) -> int:
    return apply_discount(subtotal)


def calculate_store_total(subtotal: int) -> int:
    return apply_discount(subtotal)


def main() -> None:
    for subtotal in (80, 120):
        print(f"Online: {calculate_online_total(subtotal)} credits")
        print(f"Store: {calculate_store_total(subtotal)} credits")


if __name__ == "__main__":
    main()
