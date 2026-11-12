# Tema: el entorno proporciona un parámetro sin modificar la función.
import os


def read_timeout() -> float:
    return float(os.environ.get("APP_HTTP_TIMEOUT_SECONDS", "2.0"))


if __name__ == "__main__":
    print(f"Timeout: {read_timeout()}")
