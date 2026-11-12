# Tema: compartir únicamente el contrato que todas las figuras pueden cumplir.
from abc import ABC, abstractmethod
from dataclasses import dataclass


class Shape(ABC):
    @abstractmethod
    def area(self) -> int:
        raise NotImplementedError


@dataclass(frozen=True)
class Rectangle(Shape):
    width: int
    height: int

    def area(self) -> int:
        return self.width * self.height


@dataclass(frozen=True)
class Square(Shape):
    side: int

    def area(self) -> int:
        return self.side * self.side


def total_area(shapes: list[Shape]) -> int:
    # Cualquier subtipo cumple el cálculo sin condiciones especiales por tipo.
    return sum(shape.area() for shape in shapes)


def main() -> None:
    shapes: list[Shape] = [Rectangle(4, 5), Square(4)]
    for shape in shapes:
        print(f"{type(shape).__name__} area: {shape.area()}")
    print(f"Total area: {total_area(shapes)}")


if __name__ == "__main__":
    main()
