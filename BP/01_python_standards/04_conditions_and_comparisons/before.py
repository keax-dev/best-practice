# Tema: comprobar enteros sin excluir booleanos acepta True como cantidad.
def is_valid_quantity(value: object) -> bool:
    return isinstance(value, int) and value > 0

if __name__ == "__main__":
    for value in (2, True, 0, None):
        print(f"{value!r}: {is_valid_quantity(value)}")
