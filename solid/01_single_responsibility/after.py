# Tema: separar el cálculo de una factura de su representación textual.
from dataclasses import dataclass


@dataclass(frozen=True)
class Invoice:
    prices: tuple[int, ...]

    def calculate_total(self) -> int:
        return sum(self.prices)


class InvoiceRenderer:
    def render(self, invoice: Invoice) -> str:
        # El formato puede cambiar sin modificar las reglas de la factura.
        return f"Invoice total: {invoice.calculate_total()} credits"


def main() -> None:
    invoice = Invoice((40, 60))
    print(InvoiceRenderer().render(invoice))


if __name__ == "__main__":
    main()
