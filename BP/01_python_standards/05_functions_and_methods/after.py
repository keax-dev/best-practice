# Tema: self usa los datos del objeto y cls construye una instancia de su clase.
from dataclasses import dataclass


@dataclass(frozen=True)
class Order:
    unit_price: int
    quantity: int

    def total(self) -> int:
        return self.unit_price * self.quantity

    @classmethod
    def from_values(cls, unit_price: int, quantity: int) -> "Order":
        return cls(unit_price, quantity)


if __name__ == "__main__":
    print(Order.from_values(5, 2).total())
