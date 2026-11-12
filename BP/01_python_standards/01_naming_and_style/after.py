# Tema: los nombres explican la intención y los tipos documentan los argumentos.
def calculate_total(unit_price: int, quantity: int) -> int:
    return unit_price * quantity


if __name__ == "__main__":
    print(calculate_total(5, 2))
