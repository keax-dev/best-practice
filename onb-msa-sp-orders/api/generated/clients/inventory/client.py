# Generado desde OpenAPI. No editar; ejecutar scripts/generate_apis.py.
import requests

from api.generated.clients.inventory.models.deduction_input import (
    DeductionInput,
    DeductionInputSchema,
)


class InventoryClient:
    def __init__(
        self, base_url: str, timeout: tuple[float, float], headers: dict[str, str]
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.headers = headers

    def deduct_inventory(self, body: DeductionInput) -> requests.Response:
        return requests.post(
            self.base_url + "/api/v1/inventories/deductions",
            json=DeductionInputSchema().dump(body),
            timeout=self.timeout,
            headers=self.headers,
            allow_redirects=False,
        )
