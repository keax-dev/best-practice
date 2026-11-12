# Tema: una capacidad inyectada permite preparar respuestas sin red.
from collections.abc import Callable


def can_order(product_id: int, quantity: int, lookup: Callable[[int], int]) -> bool:
    return lookup(product_id) >= quantity


if __name__ == "__main__":
    print(can_order(1, 2, lambda product_id: 10))
