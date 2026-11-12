# Tema: agregar modalidades de envío sin editar el consumidor de sus tarifas.
from abc import ABC, abstractmethod


class ShippingMethod(ABC):
    @abstractmethod
    def cost(self) -> int:
        raise NotImplementedError


class StandardShipping(ShippingMethod):
    def cost(self) -> int:
        return 5


class ExpressShipping(ShippingMethod):
    def cost(self) -> int:
        return 12


class StorePickup(ShippingMethod):
    def cost(self) -> int:
        return 0


def shipping_cost(method: ShippingMethod) -> int:
    # El consumidor depende del contrato, no de una lista de tipos concretos.
    return method.cost()


def main() -> None:
    methods = {
        "standard": StandardShipping(),
        "express": ExpressShipping(),
        "pickup": StorePickup(),
    }
    for name, method in methods.items():
        print(f"{name}: {shipping_cost(method)} credits")


if __name__ == "__main__":
    main()
