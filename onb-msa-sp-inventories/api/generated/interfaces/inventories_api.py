# Generado desde OpenAPI. No editar; ejecutar scripts/generate_apis.py.
from abc import ABC, abstractmethod

from api.generated.models.deduction import Deduction
from api.generated.models.deduction_input import DeductionInput
from api.generated.models.health import Health
from api.generated.models.product import Product


class InventoryAPI(ABC):
    @abstractmethod
    def deduct_inventory(
        self, body: DeductionInput, x_user_id: str, x_user_role: str
    ) -> Deduction:
        """Implementar la operación deduct_inventory del contrato."""
        raise NotImplementedError

    @abstractmethod
    def get_health(self) -> Health:
        """Implementar la operación get_health del contrato."""
        raise NotImplementedError

    @abstractmethod
    def get_inventory(
        self, product_id: int, x_user_id: str, x_user_role: str
    ) -> Product:
        """Implementar la operación get_inventory del contrato."""
        raise NotImplementedError

    @abstractmethod
    def list_inventories(self, x_user_id: str, x_user_role: str) -> list[Product]:
        """Implementar la operación list_inventories del contrato."""
        raise NotImplementedError
