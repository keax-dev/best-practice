# Tema: una demostración manual cubre solo una cantidad.
def is_positive_quantity(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value > 0

if __name__ == "__main__":
    print(is_positive_quantity(2))
