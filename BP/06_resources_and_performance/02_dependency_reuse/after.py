# Tema: la misma dependencia se reutiliza durante el lote.
class CatalogClient:
    def lookup(self, product_id: int) -> str:
        return f"Product {product_id}"


def process(ids: list[int], client: CatalogClient) -> list[str]:
    return [client.lookup(product_id) for product_id in ids]


if __name__ == "__main__":
    client = CatalogClient()
    print(process([1, 2, 3], client))
    print("Client instances: 1")
