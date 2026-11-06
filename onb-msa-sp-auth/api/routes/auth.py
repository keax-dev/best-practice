# Tema: implementar la interfaz generada sin repetir rutas ni esquemas del contrato.
from api.generated.interfaces.auth_api import AuthAPI
from api.generated.models.health import Health
from api.generated.models.login_input import LoginInput
from api.generated.models.token import Token
from api.services.auth import AuthService


class AuthAPIImpl(AuthAPI):
    def __init__(self, service: AuthService, service_name: str) -> None:
        self.service = service
        self.service_name = service_name

    def login(self, body: LoginInput) -> Token:
        # La lógica sigue independiente de los DTO utilizados por HTTP.
        result = self.service.login(username=body.username, password=body.password)
        return Token(**result)

    def get_health(self) -> Health:
        return Health(status="ok", service=self.service_name)
