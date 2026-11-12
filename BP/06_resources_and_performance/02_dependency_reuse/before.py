# Tema: cada elemento reconstruye una dependencia simulada.
class CatalogClient:
    def lookup(self, product_id: int) -> str:
        return f"Product {product_id}"

def process(ids: list[int]) -> tuple[list[str], int]:
    results = []
    for product_id in ids:
        results.append(CatalogClient().lookup(product_id))
    return results, len(ids)

if __name__ == "__main__":
    print(process([1, 2, 3]))
