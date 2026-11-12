# Tema: el circuito abierto falla rápido y permite una prueba tras el enfriamiento.
from collections.abc import Callable


class CircuitOpenError(RuntimeError):
    pass


class CircuitBreaker:
    def __init__(self, clock: Callable[[], float], threshold: int = 2, cooldown: float = 5.0) -> None:
        if threshold < 1 or cooldown <= 0:
            raise ValueError("Invalid circuit settings")
        self.clock, self.threshold, self.cooldown = clock, threshold, cooldown
        self.failures = 0
        self.opened_at = 0.0
        self.state = "CLOSED"

    def call(self, operation: Callable[[], str]) -> str:
        if self.state == "OPEN":
            if self.clock() - self.opened_at < self.cooldown:
                raise CircuitOpenError("Circuit is open")
            self.state = "HALF_OPEN"
        try:
            result = operation()
        except ConnectionError:
            self.failures += 1
            if self.state == "HALF_OPEN" or self.failures >= self.threshold:
                self.state, self.opened_at = "OPEN", self.clock()
            raise
        self.state, self.failures = "CLOSED", 0
        return result


if __name__ == "__main__":
    now = [0.0]
    circuit = CircuitBreaker(lambda: now[0])

    def unavailable() -> str:
        raise ConnectionError("Unavailable")

    for attempt in range(3):
        try:
            circuit.call(unavailable)
        except (ConnectionError, CircuitOpenError) as error:
            print(type(error).__name__, circuit.state)
    now[0] = 5.0
    print(circuit.call(lambda: "Recovered"), circuit.state)
