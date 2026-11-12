# Tema: expresar el significado de los datos y las operaciones mediante sus nombres.
def calculate_order_total(
    unit_price: int, quantity: int, discount_amount: int
) -> int:
    return unit_price * quantity - discount_amount


def main() -> None:
    unit_price = 25
    quantity = 4
    discount_amount = 10
    total = calculate_order_total(unit_price, quantity, discount_amount)
    print(f"Order total: {total} credits")


if __name__ == "__main__":
    main()
