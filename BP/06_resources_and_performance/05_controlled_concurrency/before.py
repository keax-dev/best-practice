# Tema: un hilo por elemento no expresa un límite para cargas grandes.
from threading import Thread

def process(value: int) -> None:
    return None

if __name__ == "__main__":
    workers = [Thread(target=process, args=(value,)) for value in range(6)]
    for worker in workers:
        worker.start()
    for worker in workers:
        worker.join()
    print(f"Threads created: {len(workers)}")
