# Tema: una captura amplia convierte cualquier fallo en el mismo resultado.
def parse_quantity(raw: str) -> int | None:
    try:
        return int(raw)
    except Exception:
        return None

if __name__ == "__main__":
    print(parse_quantity("coffee"))
