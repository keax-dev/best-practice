# Tema: una instancia puede estar viva pero no lista para tráfico.
from dataclasses import dataclass


@dataclass(frozen=True)
class HealthState:
    process_healthy: bool
    initialized: bool
    dependency_ready: bool


def liveness(state: HealthState) -> bool:
    return state.process_healthy


def readiness(state: HealthState) -> bool:
    return state.process_healthy and state.initialized and state.dependency_ready


if __name__ == "__main__":
    state = HealthState(True, True, False)
    print(f"Live: {liveness(state)}; ready: {readiness(state)}")
