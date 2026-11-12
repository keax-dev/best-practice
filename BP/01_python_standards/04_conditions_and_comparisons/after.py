# Tema: una condición expresa exactamente los valores aceptados.
def is_valid_quantity(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def first_or_default(values: list[str] | None) -> str:
    if values is None:
        return "not provided"
    if not values:
        return "empty"
    return values[0]


if __name__ == "__main__":
    for value in (2, True, 0, None):
        print(f"{value!r}: {is_valid_quantity(value)}")
    print(first_or_default(None))
    print(first_or_default([]))
