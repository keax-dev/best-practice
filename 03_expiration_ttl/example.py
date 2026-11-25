# TTL: dejar de servir un precio cuando vence su tiempo de vida.

from collections.abc import Callable
from math import isfinite
from time import monotonic, sleep


class TTLCache:
    def __init__(self, ttl_seconds: float, clock: Callable[[], float] = monotonic) -> None:
        if not isfinite(ttl_seconds) or ttl_seconds <= 0:
            raise ValueError("TTL must be finite and positive")
        self.ttl_seconds = ttl_seconds
        self.clock = clock
        self.entries: dict[int, tuple[int, float]] = {}

    def set(self, product_id: int, price: int) -> None:
        self.entries[product_id] = (price, self.clock() + self.ttl_seconds)

    def get(self, product_id: int) -> int | None:
        entry = self.entries.get(product_id)
        if entry is None:
            return None
        price, expires_at = entry
        if self.clock() >= expires_at:
            del self.entries[product_id]
            return None
        return price


def main() -> None:
    cache = TTLCache(ttl_seconds=0.1)
    cache.set(1, 1250)
    print(f"Before expiration: {cache.get(1)}")
    sleep(0.15)  # Solo la demostración espera; las pruebas avanzan un reloj controlado.
    print(f"After expiration: {cache.get(1)}")


if __name__ == "__main__":
    main()
