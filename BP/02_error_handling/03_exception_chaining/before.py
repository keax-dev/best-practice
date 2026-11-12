# Tema: suprimir la causa dificulta rastrear el dato que falló.
class InvalidQuantityError(ValueError):
    pass

def parse_quantity(raw: str) -> int:
    try:
        return int(raw)
    except ValueError:
        raise InvalidQuantityError("Invalid quantity") from None

if __name__ == "__main__":
    try:
        parse_quantity("coffee")
    except InvalidQuantityError as error:
        print(f"Explicit cause: {error.__cause__}")
