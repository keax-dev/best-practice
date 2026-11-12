# Tema: representar el dato de negocio sin importar Flask.
from dataclasses import dataclass


@dataclass(frozen=True)
class Order:
    id: str
    quantity: int
