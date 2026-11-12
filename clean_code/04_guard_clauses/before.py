# Tema: la anidación oculta el camino que confirma un pedido.
def confirm_order(is_active: bool, quantity: int, stock: int) -> str:
    if is_active:
        if quantity > 0:
            if stock >= quantity:
                return "CONFIRMED"
            else:
                return "INSUFFICIENT_STOCK"
        else:
            return "INVALID_QUANTITY"
    else:
        return "INACTIVE_USER"


def main() -> None:
    for arguments in ((False, 2, 10), (True, 0, 10), (True, 12, 10), (True, 2, 10)):
        print(confirm_order(*arguments))


if __name__ == "__main__":
    main()
