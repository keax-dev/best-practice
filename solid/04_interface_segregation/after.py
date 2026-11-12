# Tema: dividir los contratos según las capacidades que necesita cada consumidor.
from abc import ABC, abstractmethod


class Workable(ABC):
    @abstractmethod
    def work(self) -> str:
        raise NotImplementedError


class Eater(ABC):
    @abstractmethod
    def eat(self) -> str:
        raise NotImplementedError


class HumanWorker(Workable, Eater):
    def work(self) -> str:
        return "Human working"

    def eat(self) -> str:
        return "Human eating"


class RobotWorker(Workable):
    def work(self) -> str:
        return "Robot working"


def run_shift(workers: list[Workable]) -> None:
    for worker in workers:
        print(worker.work())


def serve_lunch(eaters: list[Eater]) -> None:
    for eater in eaters:
        print(eater.eat())


def main() -> None:
    human = HumanWorker()
    run_shift([human, RobotWorker()])
    serve_lunch([human])


if __name__ == "__main__":
    main()
