# Tema: los comentarios que repiten el código dejan sin explicar las decisiones.
from datetime import date


def can_cancel_order(created_on: date, requested_on: date) -> bool:
    # Resta dos fechas.
    days = (requested_on - created_on).days
    # Devuelve si el valor está entre cero y siete.
    return 0 <= days <= 7


def main() -> None:
    created_on = date(2026, 1, 1)
    for requested_on in (date(2026, 1, 1), date(2026, 1, 8), date(2026, 1, 9)):
        print(f"{requested_on}: {can_cancel_order(created_on, requested_on)}")


if __name__ == "__main__":
    main()
