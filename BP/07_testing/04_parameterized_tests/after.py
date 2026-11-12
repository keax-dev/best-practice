# Tema: una regla puede verificarse con una tabla explícita de casos.
def is_positive_quantity(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


if __name__ == "__main__":
    for value in (2, 0, -1, True, "2"):
        print(f"{value!r}: {is_positive_quantity(value)}")
