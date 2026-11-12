# Tema: una caché pequeña aplica capacidad y vencimiento con un reloj controlable.
import math
from collections import OrderedDict
from collections.abc import Callable


class BoundedCache:
    def __init__(self, capacity: int, ttl: float, clock: Callable[[], float]) -> None:
        if capacity < 1 or not math.isfinite(ttl) or ttl <= 0:
            raise ValueError("Capacity and TTL must be positive")
        self.capacity = capacity
        self.ttl = ttl
        self.clock = clock
        self.items: OrderedDict[str, tuple[float, str]] = OrderedDict()

    def put(self, key: str, value: str) -> None:
        self.items.pop(key, None)
        self.items[key] = (self.clock() + self.ttl, value)
        while len(self.items) > self.capacity:
            self.items.popitem(last=False)

    def get(self, key: str) -> str | None:
        entry = self.items.get(key)
        if entry is None:
            return None
        expires_at, value = entry
        if self.clock() >= expires_at:
            del self.items[key]
            return None
        return value


if __name__ == "__main__":
    now = [0.0]
    cache = BoundedCache(2, 5.0, lambda: now[0])
    for key in ("one", "two", "three"):
        cache.put(key, key)
    print(f"Items retained: {len(cache.items)}")
    print(f"Evicted: {cache.get('one')}")
    now[0] = 5.0
    print(f"Expired: {cache.get('three')}")
