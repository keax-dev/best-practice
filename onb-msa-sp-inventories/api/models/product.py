# Tema: representar productos y resultados sin depender de HTTP.
from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    id: int
    name: str
    stock: int


@dataclass(frozen=True)
class Deduction:
    order_id: str
    product_id: int
    quantity: int
    remaining_stock: int
