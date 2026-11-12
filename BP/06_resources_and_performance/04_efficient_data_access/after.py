# Tema: una consulta por lote recupera los datos requeridos.
def product_names(ids: list[int]) -> tuple[list[str], int]:
    if not ids:
        return [], 0
    names_by_id = {product_id: f"Product {product_id}" for product_id in ids}
    return [names_by_id[product_id] for product_id in ids], 1


if __name__ == "__main__":
    print(product_names([1, 2, 3]))
