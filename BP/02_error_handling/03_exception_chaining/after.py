# Tema: encadenar excepciones conserva el origen del problema.
class InvalidQuantityError(ValueError):
    pass


def parse_quantity(raw: str) -> int:
    try:
        return int(raw)
    except ValueError as error:
        raise InvalidQuantityError("Invalid quantity") from error


if __name__ == "__main__":
    try:
        parse_quantity("coffee")
    except InvalidQuantityError as error:
        print(f"Explicit cause: {type(error.__cause__).__name__}")
