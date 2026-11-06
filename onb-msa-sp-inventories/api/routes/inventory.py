# Tema: implementar las operaciones generadas sin repetir rutas ni reglas de entrada.
from uuid import UUID

from api.generated.interfaces.inventories_api import InventoryAPI
from api.generated.models.deduction import Deduction as DeductionResponse
from api.generated.models.deduction_input import DeductionInput
from api.generated.models.health import Health
from api.generated.models.product import Product as ProductResponse
from api.models.product import Product
from api.services.inventory import InventoryService


def to_response(product: Product) -> ProductResponse:
    return ProductResponse(id=product.id, name=product.name, stock=product.stock)


class InventoryAPIImpl(InventoryAPI):
    def __init__(self, service: InventoryService, service_name: str) -> None:
        self.service = service
        self.service_name = service_name

    def list_inventories(
        self, x_user_id: str, x_user_role: str
    ) -> list[ProductResponse]:
        return [to_response(product) for product in self.service.list_all()]

    def get_inventory(
        self, product_id: int, x_user_id: str, x_user_role: str
    ) -> ProductResponse:
        return to_response(self.service.get(product_id))

    def deduct_inventory(
        self, body: DeductionInput, x_user_id: str, x_user_role: str
    ) -> DeductionResponse:
        result = self.service.deduct(str(body.order_id), body.product_id, body.quantity)
        return DeductionResponse(
            order_id=UUID(result.order_id),
            product_id=result.product_id,
            quantity=result.quantity,
            remaining_stock=result.remaining_stock,
        )

    def get_health(self) -> Health:
        return Health(status="ok", service=self.service_name)
