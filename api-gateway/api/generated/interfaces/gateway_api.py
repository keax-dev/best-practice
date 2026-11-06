# Generado desde OpenAPI. No editar; ejecutar scripts/generate_apis.py.
from abc import ABC, abstractmethod
from uuid import UUID

from flask import Response

from api.generated.models.deduction import Deduction
from api.generated.models.deduction_input import DeductionInput
from api.generated.models.health import Health
from api.generated.models.login_input import LoginInput
from api.generated.models.order import Order
from api.generated.models.order_input import OrderInput
from api.generated.models.product import Product
from api.generated.models.token import Token


class GatewayAPI(ABC):
    @abstractmethod
    def create_order(self, body: OrderInput) -> Response | Order:
        """Implementar la operación create_order del contrato."""
        raise NotImplementedError

    @abstractmethod
    def deduct_inventory(self, body: DeductionInput) -> Response | Deduction:
        """Implementar la operación deduct_inventory del contrato."""
        raise NotImplementedError

    @abstractmethod
    def get_health(self) -> Response | Health:
        """Implementar la operación get_health del contrato."""
        raise NotImplementedError

    @abstractmethod
    def get_inventory(self, product_id: int) -> Response | Product:
        """Implementar la operación get_inventory del contrato."""
        raise NotImplementedError

    @abstractmethod
    def get_order(self, order_id: UUID) -> Response | Order:
        """Implementar la operación get_order del contrato."""
        raise NotImplementedError

    @abstractmethod
    def list_inventories(self) -> Response | list[Product]:
        """Implementar la operación list_inventories del contrato."""
        raise NotImplementedError

    @abstractmethod
    def list_orders(self) -> Response | list[Order]:
        """Implementar la operación list_orders del contrato."""
        raise NotImplementedError

    @abstractmethod
    def login(self, body: LoginInput) -> Response | Token:
        """Implementar la operación login del contrato."""
        raise NotImplementedError
