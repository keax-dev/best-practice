# Tema: la respuesta marca explícitamente el uso de información de respaldo.
from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class CatalogResult:
    products: tuple[str, ...]
    stale: bool


def get_catalog(fetch: Callable[[], tuple[str, ...]], cached: tuple[str, ...]) -> CatalogResult:
    try:
        return CatalogResult(fetch(), False)
    except ConnectionError:
        return CatalogResult(cached, True)


if __name__ == "__main__":

    def unavailable() -> tuple[str, ...]:
        raise ConnectionError("Catalog unavailable")

    print(get_catalog(unavailable, ("Coffee",)))
