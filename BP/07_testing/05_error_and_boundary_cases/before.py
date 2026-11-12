# Tema: el error de comparación pasa inadvertido si no pruebas el umbral.
def discounted_total(total: int) -> int:
    return total - 10 if total > 100 else total

if __name__ == "__main__":
    print(discounted_total(120))
