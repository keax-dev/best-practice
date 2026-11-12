# Tema: una función pequeña ofrece un comportamiento verificable.
def total(price: int, quantity: int) -> int:
    return price * quantity


if __name__ == "__main__":
    print(total(5, 2))
