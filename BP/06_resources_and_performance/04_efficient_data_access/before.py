# Tema: un acceso por elemento produce el patrón de consultas repetidas.
def product_names(ids: list[int]) -> tuple[list[str], int]:
    calls = 0
    names = []
    for product_id in ids:
        calls += 1
        names.append(f"Product {product_id}")
    return names, calls

if __name__ == "__main__":
    print(product_names([1, 2, 3]))
