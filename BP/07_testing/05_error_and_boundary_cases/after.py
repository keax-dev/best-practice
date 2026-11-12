# Tema: validar datos y expresar que el umbral también recibe el descuento.
def discounted_total(total: int) -> int:
    if total < 0:
        raise ValueError("Total cannot be negative")
    return total - 10 if total >= 100 else total


if __name__ == "__main__":
    for total in (99, 100, 101):
        print(discounted_total(total))
