# Tema: dos canales repiten la misma regla de descuento y pueden terminar divergentes.
def calculate_online_total(subtotal: int) -> int:
    if subtotal >= 100:
        return subtotal - 10
    return subtotal


def calculate_store_total(subtotal: int) -> int:
    if subtotal >= 100:
        return subtotal - 10
    return subtotal


def main() -> None:
    for subtotal in (80, 120):
        print(f"Online: {calculate_online_total(subtotal)} credits")
        print(f"Store: {calculate_store_total(subtotal)} credits")


if __name__ == "__main__":
    main()
