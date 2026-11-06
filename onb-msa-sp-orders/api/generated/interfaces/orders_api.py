# Generado desde OpenAPI. No editar; ejecutar scripts/generate_apis.py.
from abc import ABC, abstractmethod
from uuid import UUID

from api.generated.models.health import Health
from api.generated.models.order import Order
from api.generated.models.order_input import OrderInput


class OrdersAPI(ABC):
    @abstractmethod
    def create_order(self, body: OrderInput, x_user_id: str, x_user_role: str) -> Order:
        """Implementar la operación create_order del contrato."""
        raise NotImplementedError

    @abstractmethod
    def get_health(self) -> Health:
        """Implementar la operación get_health del contrato."""
        raise NotImplementedError

    @abstractmethod
    def get_order(self, order_id: UUID, x_user_id: str, x_user_role: str) -> Order:
        """Implementar la operación get_order del contrato."""
        raise NotImplementedError

    @abstractmethod
    def list_orders(self, x_user_id: str, x_user_role: str) -> list[Order]:
        """Implementar la operación list_orders del contrato."""
        raise NotImplementedError
