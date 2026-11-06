# Generado desde OpenAPI. No editar; ejecutar scripts/generate_apis.py.
from abc import ABC, abstractmethod

from api.generated.models.health import Health
from api.generated.models.login_input import LoginInput
from api.generated.models.token import Token


class AuthAPI(ABC):
    @abstractmethod
    def get_health(self) -> Health:
        """Implementar la operación get_health del contrato."""
        raise NotImplementedError

    @abstractmethod
    def login(self, body: LoginInput) -> Token:
        """Implementar la operación login del contrato."""
        raise NotImplementedError
