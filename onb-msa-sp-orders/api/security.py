# Tema: aceptar únicamente identidad autenticada por el gateway, sin validar JWT.
import os
import re
from hmac import compare_digest
from pathlib import Path

from flask import Flask, current_app, g, request

from api.errors import BusinessError


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


def authorize_request() -> None:
    if request.path == "/health":
        return
    supplied = request.headers.get("X-Internal-Key", "")
    if not supplied or not compare_digest(
        supplied.encode(), current_app.config["INTERNAL_API_KEY"].encode()
    ):
        raise BusinessError(
            "AUTH_REQUIRED", "Se requiere la credencial del gateway", 401
        )
    user_id = request.headers.get("X-User-Id", "")
    role = request.headers.get("X-User-Role", "")
    if not re.fullmatch(r"[a-zA-Z0-9_-]{1,64}", user_id) or role not in {
        "ADMIN",
        "CLIENT",
    }:
        raise BusinessError("FORBIDDEN", "Identidad interna inválida", 403)
    g.user_id, g.user_role = user_id, role
