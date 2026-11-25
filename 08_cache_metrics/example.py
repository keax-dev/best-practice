# Métricas: contar aciertos, fallos de caché e intentos de carga al origen.

from collections.abc import Callable


class MeasuredCache:
    def __init__(self, loader: Callable[[int], int]) -> None:
        self.loader = loader
        self.entries: dict[int, int] = {}
        self.hits = 0
        self.misses = 0
        self.source_calls = 0
        self.load_errors = 0

    def get_price(self, product_id: int) -> int:
        if product_id in self.entries:
            self.hits += 1
            return self.entries[product_id]
        self.misses += 1
        self.source_calls += 1
        try:
            price = self.loader(product_id)
        except (KeyError, TimeoutError, ConnectionError):
            self.load_errors += 1
            raise  # Se cuenta el fallo sin ocultarlo ni almacenarlo como un dato válido.
        self.entries[product_id] = price
        return price

    def hit_ratio(self) -> float:
        requests = self.hits + self.misses
        return self.hits / requests if requests else 0.0


def main() -> None:
    prices = {1: 1250, 2: 700}
    cache = MeasuredCache(prices.__getitem__)
    for product_id in (1, 1, 2, 1):
        print(f"Product {product_id}: {cache.get_price(product_id)} cents")
    print(f"Hits: {cache.hits} | Misses: {cache.misses}")
    print(f"Source calls: {cache.source_calls} | Load errors: {cache.load_errors}")
    print(f"Hit ratio: {cache.hit_ratio():.0%}")


if __name__ == "__main__":
    main()
