# Tema: capturar cualquier excepción y devolver cero oculta las entradas inválidas.
def parse_quantity(raw_quantity: str) -> int:
    try:
        quantity = int(raw_quantity)
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        return quantity
    except Exception:
        # El llamador no sabe si recibió un dato válido o si hubo un fallo.
        return 0


def main() -> None:
    for raw_quantity in ("3", "coffee", "0"):
        print(f"Quantity: {parse_quantity(raw_quantity)}")


if __name__ == "__main__":
    main()
