# Invalidación: actualizar el origen y retirar la copia anterior de la caché.


class ProductCatalog:
    def __init__(self) -> None:
        self.prices = {1: 1250}
        self.cache: dict[int, int] = {}
        self.source_calls = 0

    def get_price(self, product_id: int) -> int:
        if product_id not in self.cache:
            self.source_calls += 1
            self.cache[product_id] = self.prices[product_id]
        return self.cache[product_id]

    def update_price(self, product_id: int, price: int) -> None:
        if type(price) is not int or price < 0:
            raise ValueError("Price must be a nonnegative integer")
        if product_id not in self.prices:
            raise KeyError(product_id)
        self.prices[product_id] = price
        self.cache.pop(product_id, None)  # Se invalida después de completar la escritura.


def main() -> None:
    catalog = ProductCatalog()
    print(f"Before update: {catalog.get_price(1)} cents")
    catalog.update_price(1, 1500)
    print(f"Cached immediately after update: {1 in catalog.cache}")
    print(f"After update: {catalog.get_price(1)} cents")
    print(f"Source calls: {catalog.source_calls}")


if __name__ == "__main__":
    main()
