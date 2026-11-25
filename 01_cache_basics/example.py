# Caché básica: reutilizar el precio de un producto y observar hits y misses.

from time import perf_counter, sleep


class ProductCatalog:
    def __init__(self) -> None:
        self.prices = {1: 1250, 2: 700}
        self.cache: dict[int, int] = {}
        self.source_calls = 0

    def get_price(self, product_id: int) -> int:
        if product_id in self.cache:
            print("Cache HIT")
            return self.cache[product_id]

        print("Cache MISS")
        self.source_calls += 1
        sleep(0.03)  # Simula la espera de una consulta externa, sin usar una base de datos.
        price = self.prices[product_id]
        self.cache[product_id] = price
        return price


def main() -> None:
    catalog = ProductCatalog()
    for _ in range(2):
        started_at = perf_counter()
        price = catalog.get_price(1)
        print(f"Price: {price} cents | Elapsed: {perf_counter() - started_at:.6f}s")
    print(f"Source calls: {catalog.source_calls}")


if __name__ == "__main__":
    main()
