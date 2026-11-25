# LRU: limitar entradas y expulsar la que lleva más tiempo sin utilizarse.

from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity: int) -> None:
        if type(capacity) is not int or capacity <= 0:
            raise ValueError("Capacity must be a positive integer")
        self.capacity = capacity
        self.entries: OrderedDict[int, int] = OrderedDict()

    def get(self, product_id: int) -> int | None:
        if product_id not in self.entries:
            return None
        self.entries.move_to_end(product_id)
        return self.entries[product_id]

    def set(self, product_id: int, price: int) -> None:
        self.entries[product_id] = price
        self.entries.move_to_end(product_id)
        if len(self.entries) > self.capacity:
            self.entries.popitem(last=False)  # El primer elemento es el menos reciente.


def main() -> None:
    cache = LRUCache(capacity=2)
    cache.set(1, 1250)
    cache.set(2, 700)
    cache.get(1)
    cache.set(3, 900)
    print(f"Product 2 after eviction: {cache.get(2)}")
    print(f"Keys from oldest to newest: {list(cache.entries)}")


if __name__ == "__main__":
    main()
