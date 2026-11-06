# Tema: comprobar credenciales y emitir un JWT firmado con RS256.
from datetime import UTC, datetime, timedelta

import jwt
from werkzeug.security import check_password_hash

from api.errors import BusinessError
from api.repositories.user import UserRepository


class AuthService:
    def __init__(
        self,
        repository: UserRepository,
        private_key: str,
        issuer: str,
        audience: str,
        lifetime: int,
    ) -> None:
        self.repository = repository
        self.private_key = private_key
        self.issuer = issuer
        self.audience = audience
        self.lifetime = lifetime

    def login(self, username: str, password: str) -> dict:
        user = self.repository.find(username)
        # Usar un hash real también para usuarios inexistentes evita una salida inmediata.
        candidate = user or self.repository.find("admin")
        valid = check_password_hash(candidate.password_hash, password)
        if user is None or not valid:
            raise BusinessError(
                "INVALID_CREDENTIALS", "Usuario o contraseña incorrectos", 401
            )
        now = datetime.now(UTC)
        claims = {
            "sub": user.id,
            "role": user.role,
            "iss": self.issuer,
            "aud": self.audience,
            "iat": now,
            "exp": now + timedelta(seconds=self.lifetime),
        }
        token = jwt.encode(claims, self.private_key, algorithm="RS256")
        return {
            "access_token": token,
            "token_type": "Bearer",
            "expires_in": self.lifetime,
        }
