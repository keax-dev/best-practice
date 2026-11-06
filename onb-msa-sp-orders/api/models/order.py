# Tema: pedido inmutable con identificador y fecha UTC.
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Order:
    id: str
    user_id: str
    product_id: int
    quantity: int
    status: str
    reason: str | None
    created_at: datetime
