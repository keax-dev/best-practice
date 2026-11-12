# Tema: usar nombres para explicar operaciones y comentarios para justificar reglas.
from datetime import date

MAX_CANCELLATION_DAYS = 7


def can_cancel_order(created_on: date, requested_on: date) -> bool:
    elapsed_days = (requested_on - created_on).days
    # La política de este ejemplo incluye el séptimo día y usa días calendario.
    # Una fecha anterior a la compra no representa una solicitud válida.
    return 0 <= elapsed_days <= MAX_CANCELLATION_DAYS


def main() -> None:
    created_on = date(2026, 1, 1)
    for requested_on in (date(2026, 1, 1), date(2026, 1, 8), date(2026, 1, 9)):
        print(f"{requested_on}: {can_cancel_order(created_on, requested_on)}")


if __name__ == "__main__":
    main()
