# Pruebas de comportamiento para los ejemplos independientes de manejo de caché.

from concurrent.futures import ThreadPoolExecutor
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from threading import Barrier
from types import ModuleType
import unittest


def load_example(folder: str) -> ModuleType:
    path = Path(__file__).resolve().parents[1] / folder / "example.py"
    spec = spec_from_file_location(folder, path)
    if spec is None or spec.loader is None:
        raise ImportError(str(path))
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CacheTests(unittest.TestCase):
    def test_basic_cache_reads_source_once(self) -> None:
        module = load_example("01_cache_basics")
        catalog = module.ProductCatalog()
        self.assertEqual(catalog.get_price(1), 1250)
        self.assertEqual(catalog.get_price(1), 1250)
        self.assertEqual(catalog.source_calls, 1)

    def test_memoization_distinguishes_arguments_and_clears(self) -> None:
        module = load_example("02_memoization")
        total = module.calculate_total
        self.assertEqual(total(1250, 2), 2500)
        self.assertEqual(total(1250, 2), 2500)
        self.assertEqual(total(1250, 3), 3750)
        self.assertEqual((total.cache_info().hits, total.cache_info().misses), (1, 2))
        total.cache_clear()
        self.assertEqual(total.cache_info().currsize, 0)

    def test_ttl_expires_at_boundary_without_sliding_on_read(self) -> None:
        module = load_example("03_expiration_ttl")
        current_time = [10.0]
        cache = module.TTLCache(5.0, clock=lambda: current_time[0])
        cache.set(1, 0)
        current_time[0] = 14.0
        self.assertEqual(cache.get(1), 0)
        current_time[0] = 15.0
        self.assertIsNone(cache.get(1))
        self.assertNotIn(1, cache.entries)
        self.assertIsNone(cache.get(99))

    def test_ttl_replacement_gets_new_deadline(self) -> None:
        module = load_example("03_expiration_ttl")
        current_time = [0.0]
        cache = module.TTLCache(5, clock=lambda: current_time[0])
        cache.set(1, 1250)
        current_time[0] = 4.0
        cache.set(1, 1500)
        current_time[0] = 5.0
        self.assertEqual(cache.get(1), 1500)
        current_time[0] = 9.0
        self.assertIsNone(cache.get(1))

    def test_ttl_rejects_invalid_durations(self) -> None:
        module = load_example("03_expiration_ttl")
        for duration in (0, -1, float("inf"), float("nan")):
            with self.subTest(duration=duration), self.assertRaises(ValueError):
                module.TTLCache(duration)

    def test_lru_read_preserves_recent_product(self) -> None:
        module = load_example("04_eviction_lru")
        cache = module.LRUCache(2)
        cache.set(1, 1250)
        cache.set(2, 700)
        self.assertEqual(cache.get(1), 1250)
        cache.set(3, 900)
        self.assertIsNone(cache.get(2))
        self.assertEqual(cache.get(1), 1250)
        self.assertEqual(cache.get(3), 900)

    def test_lru_update_does_not_evict_another_product(self) -> None:
        module = load_example("04_eviction_lru")
        cache = module.LRUCache(2)
        cache.set(1, 1250)
        cache.set(2, 700)
        cache.set(1, 0)
        self.assertEqual(len(cache.entries), 2)
        self.assertEqual(cache.get(1), 0)
        self.assertEqual(cache.get(2), 700)

    def test_lru_rejects_invalid_capacities(self) -> None:
        module = load_example("04_eviction_lru")
        for capacity in (0, -1, True, 1.5):
            with self.subTest(capacity=capacity), self.assertRaises(ValueError):
                module.LRUCache(capacity)

    def test_cache_aside_loads_each_missing_product_once(self) -> None:
        module = load_example("05_cache_aside")
        repository = module.ProductRepository()
        service = module.ProductService(repository)
        for product_id, price in ((1, 1250), (1, 1250), (2, 700)):
            self.assertEqual(service.get_price(product_id), price)
        self.assertEqual(repository.calls, 2)

    def test_cache_aside_does_not_cache_missing_product(self) -> None:
        module = load_example("05_cache_aside")
        repository = module.ProductRepository()
        service = module.ProductService(repository)
        with self.assertRaises(KeyError):
            service.get_price(99)
        repository.prices[99] = 300
        self.assertEqual(service.get_price(99), 300)
        self.assertEqual(repository.calls, 2)

    def test_invalidation_reloads_new_price(self) -> None:
        module = load_example("06_invalidation")
        catalog = module.ProductCatalog()
        self.assertEqual(catalog.get_price(1), 1250)
        catalog.update_price(1, 1500)
        self.assertNotIn(1, catalog.cache)
        self.assertEqual(catalog.get_price(1), 1500)
        self.assertEqual(catalog.source_calls, 2)

    def test_invalid_update_preserves_source_and_cache(self) -> None:
        module = load_example("06_invalidation")
        catalog = module.ProductCatalog()
        catalog.get_price(1)
        for price in (-1, True, 1.5):
            with self.subTest(price=price), self.assertRaises(ValueError):
                catalog.update_price(1, price)
        self.assertEqual(catalog.prices[1], 1250)
        self.assertEqual(catalog.cache[1], 1250)
        with self.assertRaises(KeyError):
            catalog.update_price(99, 500)
        self.assertNotIn(99, catalog.prices)

    def test_concurrent_requests_load_source_once(self) -> None:
        module = load_example("07_concurrent_access")
        cache = module.LockedCache(module.load_price)
        barrier = Barrier(6, timeout=5)

        def request_price() -> int:
            barrier.wait()
            return cache.get_price(1)

        with ThreadPoolExecutor(max_workers=6) as executor:
            futures = [executor.submit(request_price) for _ in range(6)]
            self.assertEqual([future.result(timeout=5) for future in futures], [1250] * 6)
        self.assertEqual(cache.source_calls, 1)

    def test_failed_concurrent_load_allows_later_retry(self) -> None:
        module = load_example("07_concurrent_access")
        calls = []

        def load_price(product_id: int) -> int:
            calls.append(product_id)
            if len(calls) == 1:
                raise TimeoutError("Source unavailable")
            return 1250

        cache = module.LockedCache(load_price)
        with self.assertRaises(TimeoutError):
            cache.get_price(1)
        self.assertNotIn(1, cache.entries)
        with ThreadPoolExecutor(max_workers=1) as executor:
            self.assertEqual(executor.submit(cache.get_price, 1).result(timeout=5), 1250)
        self.assertEqual(cache.source_calls, 2)

    def test_metrics_include_hits_misses_and_empty_ratio(self) -> None:
        module = load_example("08_cache_metrics")
        cache = module.MeasuredCache({1: 1250, 2: 700}.__getitem__)
        self.assertEqual(cache.hit_ratio(), 0)
        for product_id in (1, 1, 2, 1):
            cache.get_price(product_id)
        self.assertEqual((cache.hits, cache.misses, cache.source_calls), (2, 2, 2))
        self.assertEqual(cache.hit_ratio(), 0.5)
        self.assertEqual(cache.load_errors, 0)

    def test_metrics_count_failed_load_without_caching_error(self) -> None:
        module = load_example("08_cache_metrics")
        prices = {}
        cache = module.MeasuredCache(prices.__getitem__)
        with self.assertRaises(KeyError):
            cache.get_price(1)
        self.assertEqual((cache.misses, cache.source_calls, cache.load_errors), (1, 1, 1))
        self.assertNotIn(1, cache.entries)
        prices[1] = 0
        self.assertEqual(cache.get_price(1), 0)
        self.assertEqual(cache.get_price(1), 0)
        self.assertEqual((cache.hits, cache.misses, cache.source_calls), (1, 2, 2))


if __name__ == "__main__":
    unittest.main()
