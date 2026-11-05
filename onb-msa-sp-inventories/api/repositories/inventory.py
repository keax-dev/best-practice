# Tema: descuento atómico e idempotente dentro de un único proceso.
from dataclasses import replace
from threading import Lock

from api.errors import BusinessError
from api.models.product import Deduction, Product


class InventoryRepository:
    def __init__(self, products: tuple[Product, ...]) -> None:
        self._products = {product.id: replace(product) for product in products}
        self._deductions: dict[str, Deduction] = {}
        self._lock = Lock()

    def list_all(self) -> list[Product]:
        with self._lock:
            return list(self._products.values())

    def get(self, product_id: int) -> Product:
        with self._lock:
            return self._find(product_id)

    def _find(self, product_id: int) -> Product:
        product = self._products.get(product_id)
        if product is None:
            raise BusinessError(
                "PRODUCT_NOT_FOUND",
                "Producto inexistente",
                404,
                {"product_id": product_id},
            )
        return product

    def deduct(self, order_id: str, product_id: int, quantity: int) -> Deduction:
        # El mismo lock cubre TODA la operación, no solo la escritura.
        with self._lock:
            previous = self._deductions.get(order_id)
            if previous is not None:
                if (previous.product_id, previous.quantity) != (product_id, quantity):
                    raise BusinessError(
                        "IDEMPOTENCY_CONFLICT",
                        "El pedido ya tiene otro descuento",
                        409,
                        {"order_id": order_id},
                    )
                return previous
            product = self._find(product_id)
            if product.stock < quantity:
                raise BusinessError(
                    "INSUFFICIENT_STOCK",
                    "Stock insuficiente",
                    409,
                    {"product_id": product_id},
                )
            remaining_stock = product.stock - quantity
            result = Deduction(order_id, product_id, quantity, remaining_stock)
            self._products[product_id] = replace(product, stock=remaining_stock)
            self._deductions[order_id] = result
            return result
