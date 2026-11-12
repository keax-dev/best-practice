# Tema: el arranque rechaza valores que no sirven como timeout.
import math


def parse_timeout(raw: str) -> float:
    value = float(raw)
    if not math.isfinite(value) or value <= 0:
        raise ValueError("Timeout must be finite and positive")
    return value


if __name__ == "__main__":
    for raw in ("2", "nan", "0"):
        try:
            print(parse_timeout(raw))
        except ValueError as error:
            print(f"Configuration error: {error}")
