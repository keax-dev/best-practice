# Tema: expresar errores esperados y capturarlos donde se decide cómo responder.
class InvalidQuantityError(ValueError):
    pass


def parse_quantity(raw_quantity: str) -> int:
    try:
        quantity = int(raw_quantity)
    except ValueError as error:
        # Se conserva la causa original para facilitar el diagnóstico.
        raise InvalidQuantityError("Quantity must be an integer") from error
    if quantity <= 0:
        raise InvalidQuantityError("Quantity must be positive")
    return quantity


def main() -> None:
    for raw_quantity in ("3", "coffee", "0"):
        try:
            print(f"Quantity: {parse_quantity(raw_quantity)}")
        except InvalidQuantityError as error:
            print(f"Invalid input: {error}")


if __name__ == "__main__":
    main()
