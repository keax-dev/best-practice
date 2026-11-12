# Tema: ejecutar solo el camino válido deja la rama de error sin comprobar.
def classify(quantity: int) -> str:
    if quantity <= 0:
        return "INVALID"
    return "VALID"

if __name__ == "__main__":
    print(classify(2))
