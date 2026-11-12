# Tema: una subclase rompe el contrato de redimensionar ancho y alto por separado.
class Rectangle:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

    def resize(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

    def area(self) -> int:
        return self.width * self.height


class Square(Rectangle):
    def resize(self, width: int, height: int) -> None:
        # Mantener lados iguales ignora el alto solicitado por el consumidor.
        self.width = width
        self.height = width


def resize_and_report(rectangle: Rectangle) -> None:
    rectangle.resize(4, 5)
    print(f"Expected area: 20; actual area: {rectangle.area()}")


def main() -> None:
    resize_and_report(Rectangle(2, 3))
    resize_and_report(Square(2, 2))


if __name__ == "__main__":
    main()
