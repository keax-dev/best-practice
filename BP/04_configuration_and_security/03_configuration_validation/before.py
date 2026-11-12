# Tema: convertir un texto no asegura que su valor sea válido.
def parse_timeout(raw: str) -> float:
    return float(raw)

if __name__ == "__main__":
    print(parse_timeout("nan"))
