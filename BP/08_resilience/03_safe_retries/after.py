# Tema: un retry acotado se aplica a errores temporales de una consulta.
import math
import random
import time
from collections.abc import Callable


def retry_read(
    operation: Callable[[], str],
    attempts: int = 3,
    *,
    sleep: Callable[[float], None] = time.sleep,
    jitter: Callable[[], float] = random.random,
) -> str:
    if attempts < 1:
        raise ValueError("Attempts must be positive")
    for attempt in range(attempts):
        try:
            return operation()
        except ConnectionError:
            if attempt == attempts - 1:
                raise
            delay = 0.01 * (2**attempt) + jitter() * 0.005
            if not math.isfinite(delay) or delay < 0:
                raise ValueError("Invalid retry delay")
            sleep(delay)
    raise RuntimeError("Unreachable retry state")


if __name__ == "__main__":
    responses = iter([ConnectionError("Temporary"), "Catalog response"])

    def read_catalog() -> str:
        response = next(responses)
        if isinstance(response, Exception):
            raise response
        return response

    delays: list[float] = []
    print(retry_read(read_catalog, sleep=delays.append, jitter=lambda: 0.0))
    print(f"Backoff: {delays}")
