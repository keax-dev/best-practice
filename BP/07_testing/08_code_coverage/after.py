# Tema: las pruebas deben recorrer los dos resultados de la decisión.
def classify(quantity: int) -> str:
    if quantity <= 0:
        return "INVALID"
    return "VALID"


if __name__ == "__main__":
    print(classify(2))
    print(classify(0))
