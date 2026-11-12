# Tema: with garantiza el cierre aunque se produzca una excepción.
from tempfile import TemporaryFile


def demonstrate() -> bool:
    try:
        with TemporaryFile(mode="w+t", encoding="utf-8") as file:
            file.write("Coffee")
            raise ValueError("Simulated processing error")
    except ValueError:
        return file.closed


if __name__ == "__main__":
    print(f"Closed after error: {demonstrate()}")
