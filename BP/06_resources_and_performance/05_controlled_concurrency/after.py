# Tema: un pool acota trabajadores y pendientes sin crear un hilo por dato.
from concurrent.futures import ThreadPoolExecutor


def process(value: int) -> int:
    return value * 2


def process_batch(values: list[int]) -> list[int]:
    with ThreadPoolExecutor(max_workers=2) as executor:
        return list(executor.map(process, values, buffersize=2))


if __name__ == "__main__":
    print(process_batch(list(range(6))))
