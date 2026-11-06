# Tema: centralizar autenticación JWT y permisos de rutas en el gateway.
import os
import re
from hmac import compare_digest
from pathlib import Path

import jwt
from flask import Flask, current_app, g, request

from api.errors import BusinessError

DEDUCTION_PATH = "/api/v1/inventories/deductions"


def configure_security(app: Flask) -> None:
    directory = Path(app.root_path).parents[1] / ".secrets"
    for name, filename in (
        ("INTERNAL_API_KEY", "internal-api.key"),
        ("ORDERS_SERVICE_KEY", "orders-service.key"),
    ):
        path = app.config.get(name + "_FILE") or os.getenv(
            name + "_FILE", str(directory / filename)
        )
        value = (
            app.config.get(name)
            or os.getenv(name)
            or Path(path).read_text(encoding="utf-8").strip()
        )
        if len(value) < 32:
            raise ValueError(f"{name} must contain at least 32 characters")
        app.config[name] = value
    public_path = app.config.get("JWT_PUBLIC_KEY_FILE") or os.getenv(
        "JWT_PUBLIC_KEY_FILE", str(directory / "jwt-public.pem")
    )
    app.config["JWT_PUBLIC_KEY"] = app.config.get("JWT_PUBLIC_KEY") or Path(
        public_path
    ).read_text(encoding="utf-8")
    app.config.setdefault("JWT_ISSUER", os.getenv("JWT_ISSUER", "coe-auth"))
    app.config.setdefault("JWT_AUDIENCE", os.getenv("JWT_AUDIENCE", "coe-backend"))


def authorize_request() -> None:
    if request.path in {"/health", "/api/v1/auth/login"}:
        return
    authorization = request.headers.get("Authorization", "")
    service_key = request.headers.get("X-Orders-Service-Key", "")
    if service_key:
        if authorization or not compare_digest(
            service_key.encode(), current_app.config["ORDERS_SERVICE_KEY"].encode()
        ):
            raise BusinessError("INVALID_TOKEN", "Credencial interna inválida", 401)
        if request.method != "POST" or request.path != DEDUCTION_PATH:
            raise BusinessError(
                "FORBIDDEN", "Pedidos solo puede solicitar descuentos", 403
            )
        g.user_id, g.user_role = "orders-service", "SERVICE"
        return
    parts = authorization.split()
    if not authorization:
        raise BusinessError("AUTH_REQUIRED", "Se requiere un token Bearer", 401)
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise BusinessError("INVALID_TOKEN", "Token inválido", 401)
    try:
        claims = jwt.decode(
            parts[1],
            current_app.config["JWT_PUBLIC_KEY"],
            algorithms=["RS256"],
            issuer=current_app.config["JWT_ISSUER"],
            audience=current_app.config["JWT_AUDIENCE"],
            options={"require": ["sub", "role", "exp", "iat", "iss", "aud"]},
        )
        if not re.fullmatch(r"[a-zA-Z0-9_-]{1,64}", claims["sub"]) or claims[
            "role"
        ] not in {"ADMIN", "CLIENT"}:
            raise jwt.InvalidTokenError("Invalid identity")
    except jwt.ExpiredSignatureError as error:
        raise BusinessError("TOKEN_EXPIRED", "El token ha vencido", 401) from error
    except (jwt.InvalidTokenError, TypeError) as error:
        raise BusinessError("INVALID_TOKEN", "Token inválido", 401) from error
    g.user_id, g.user_role = claims["sub"], claims["role"]
    if g.user_role == "CLIENT" and not request.path.startswith("/api/v1/orders"):
        raise BusinessError(
            "FORBIDDEN", "El cliente no puede acceder a Inventario", 403
        )
