# Tema: ejecutar una operación no comprueba que el resultado sea correcto.
def total(price: int, quantity: int) -> int:
    return price * quantity

if __name__ == "__main__":
    print(total(5, 2))
