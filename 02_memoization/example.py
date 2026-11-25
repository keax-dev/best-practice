# Memoización: reutilizar un cálculo cuando se repiten sus argumentos.

from functools import lru_cache
from time import sleep


@lru_cache(maxsize=4)
def calculate_total(unit_price: int, quantity: int) -> int:
    print("Calculating total")
    sleep(0.03)  # Representa un cálculo costoso, manteniendo el ejemplo pequeño.
    return unit_price * quantity


def main() -> None:
    print(f"Total: {calculate_total(1250, 2)} cents")
    print(f"Total: {calculate_total(1250, 2)} cents")
    print(calculate_total.cache_info())
    calculate_total.cache_clear()
    print(f"After clearing: {calculate_total.cache_info()}")


if __name__ == "__main__":
    main()
