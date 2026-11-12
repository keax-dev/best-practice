# Tema: se captura únicamente el error esperado durante la conversión.
def parse_quantity(raw: str) -> int:
    return int(raw)


if __name__ == "__main__":
    try:
        print(parse_quantity("coffee"))
    except ValueError:
        print("Invalid integer")
