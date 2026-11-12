# Tema: la regla se puede reutilizar sin depender de la consola.
def calculate_total(unit_price: int, quantity: int) -> int:
    return unit_price * quantity


def display_total(total: int) -> None:
    print(f"Total: {total}")


if __name__ == "__main__":
    display_total(calculate_total(5, 2))
