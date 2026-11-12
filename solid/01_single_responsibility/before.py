# Tema: una factura mezcla las reglas de cálculo con su presentación.
from dataclasses import dataclass


@dataclass(frozen=True)
class Invoice:
    prices: tuple[int, ...]

    def calculate_total(self) -> int:
        return sum(self.prices)

    def render(self) -> str:
        # Cambiar el formato obliga a modificar la misma clase que calcula.
        return f"Invoice total: {self.calculate_total()} credits"


def main() -> None:
    invoice = Invoice((40, 60))
    print(invoice.render())


if __name__ == "__main__":
    main()
