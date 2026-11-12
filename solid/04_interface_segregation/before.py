# Tema: una interfaz obliga a un robot a implementar una operación que no necesita.
from abc import ABC, abstractmethod


class Worker(ABC):
    @abstractmethod
    def work(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def eat(self) -> str:
        raise NotImplementedError


class HumanWorker(Worker):
    def work(self) -> str:
        return "Human working"

    def eat(self) -> str:
        return "Human eating"


class RobotWorker(Worker):
    def work(self) -> str:
        return "Robot working"

    def eat(self) -> str:
        raise NotImplementedError("Robots do not eat")


def main() -> None:
    workers: list[Worker] = [HumanWorker(), RobotWorker()]
    for worker in workers:
        print(worker.work())
        try:
            print(worker.eat())
        except NotImplementedError as error:
            # Se muestra el defecto del diseño sin terminar con una traza.
            print(f"Design problem: {error}")


if __name__ == "__main__":
    main()
