# Concurrencia: coordinar varios hilos para no cargar repetidamente la misma clave.

from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier, Lock
from time import sleep


class LockedCache:
    def __init__(self, loader: Callable[[int], int]) -> None:
        self.loader = loader
        self.entries: dict[int, int] = {}
        self.lock = Lock()
        self.source_calls = 0

    def get_price(self, product_id: int) -> int:
        # El lock incluye la carga; este diseño sencillo también serializa claves distintas.
        with self.lock:
            if product_id not in self.entries:
                self.source_calls += 1
                price = self.loader(product_id)
                self.entries[product_id] = price
            return self.entries[product_id]


def load_price(product_id: int) -> int:
    sleep(0.03)
    return {1: 1250}[product_id]


def main() -> None:
    cache = LockedCache(load_price)
    barrier = Barrier(6, timeout=5)

    def request_price() -> int:
        barrier.wait()  # Hace que los seis hilos comiencen la consulta juntos.
        return cache.get_price(1)

    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = [executor.submit(request_price) for _ in range(6)]
        prices = [future.result(timeout=5) for future in futures]
    print(f"Prices: {prices}")
    print(f"Source calls: {cache.source_calls}")


if __name__ == "__main__":
    main()
