# Tema: resolver condiciones de salida al inicio y dejar visible el caso exitoso.
def confirm_order(is_active: bool, quantity: int, stock: int) -> str:
    if not is_active:
        return "INACTIVE_USER"
    if quantity <= 0:
        return "INVALID_QUANTITY"
    if stock < quantity:
        return "INSUFFICIENT_STOCK"
    return "CONFIRMED"


def main() -> None:
    # Se conserva el orden de prioridad de las validaciones del ejemplo anterior.
    for arguments in ((False, 2, 10), (True, 0, 10), (True, 12, 10), (True, 2, 10)):
        print(confirm_order(*arguments))


if __name__ == "__main__":
    main()
