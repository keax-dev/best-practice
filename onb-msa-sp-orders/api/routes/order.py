# Tema: implementar la API generada y mapear el modelo de negocio a su response.
from uuid import UUID

from api.generated.interfaces.orders_api import OrdersAPI
from api.generated.models.health import Health
from api.generated.models.order import Order as OrderResponse
from api.generated.models.order_input import OrderInput
from api.models.order import Order
from api.services.order import OrderService


def to_response(order: Order) -> OrderResponse:
    return OrderResponse(
        id=UUID(order.id),
        user_id=order.user_id,
        product_id=order.product_id,
        quantity=order.quantity,
        status=order.status,
        reason=order.reason,
        created_at=order.created_at,
    )


class OrdersAPIImpl(OrdersAPI):
    def __init__(self, service: OrderService, service_name: str) -> None:
        self.service = service
        self.service_name = service_name

    def create_order(
        self, body: OrderInput, x_user_id: str, x_user_role: str
    ) -> OrderResponse:
        # Los encabezados ya fueron autenticados y validados antes de entrar aquí.
        return to_response(
            self.service.create(body.product_id, body.quantity, user_id=x_user_id)
        )

    def list_orders(self, x_user_id: str, x_user_role: str) -> list[OrderResponse]:
        return [
            to_response(order)
            for order in self.service.list_all(x_user_id, x_user_role)
        ]

    def get_order(
        self, order_id: UUID, x_user_id: str, x_user_role: str
    ) -> OrderResponse:
        return to_response(self.service.get(str(order_id), x_user_id, x_user_role))

    def get_health(self) -> Health:
        return Health(status="ok", service=self.service_name)
