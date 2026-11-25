# Cache-aside: consultar el origen únicamente cuando falta el precio en caché.


class ProductRepository:
    def __init__(self) -> None:
        self.prices = {1: 1250, 2: 700}
        self.calls = 0

    def get_price(self, product_id: int) -> int:
        self.calls += 1
        return self.prices[product_id]


class ProductService:
    def __init__(self, repository: ProductRepository) -> None:
        self.repository = repository
        self.cache: dict[int, int] = {}

    def get_price(self, product_id: int) -> int:
        if product_id not in self.cache:
            price = self.repository.get_price(product_id)
            self.cache[product_id] = price  # Solo se almacena si la consulta tuvo éxito.
        return self.cache[product_id]


def main() -> None:
    repository = ProductRepository()
    service = ProductService(repository)
    for product_id in (1, 1, 2):
        print(f"Product {product_id}: {service.get_price(product_id)} cents")
    print(f"Source calls: {repository.calls}")


if __name__ == "__main__":
    main()
