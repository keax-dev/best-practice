# Tema: calcular y mostrar el resultado quedan mezclados.
def process_order(unit_price: int, quantity: int) -> None:
    print(f"Total: {unit_price * quantity}")

if __name__ == "__main__":
    process_order(5, 2)
