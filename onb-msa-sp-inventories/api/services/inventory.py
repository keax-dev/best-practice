# Tema: operaciones de inventario independientes de Flask.
from api.models.product import Deduction, Product
from api.repositories.inventory import InventoryRepository


class InventoryService:
    def __init__(self, repository: InventoryRepository) -> None:
        self.repository = repository

    def list_all(self) -> list[Product]:
        return self.repository.list_all()

    def get(self, product_id: int) -> Product:
        return self.repository.get(product_id)

    def deduct(self, order_id: str, product_id: int, quantity: int) -> Deduction:
        return self.repository.deduct(order_id, product_id, quantity)
