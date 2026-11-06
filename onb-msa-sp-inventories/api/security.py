# Tema: Inventario confía en la credencial interna, no en encabezados públicos.
import os
import re
from hmac import compare_digest
from pathlib import Path

from flask import Flask, current_app, request

from api.errors import BusinessError


def configure_security(app: Flask) -> None:
    directory = Path(app.root_path).parents[1] / ".secrets"
    path = app.config.get("INTERNAL_API_KEY_FILE") or os.getenv(
        "INTERNAL_API_KEY_FILE", str(directory / "internal-api.key")
    )
    value = (
        app.config.get("INTERNAL_API_KEY")
        or os.getenv("INTERNAL_API_KEY")
        or Path(path).read_text(encoding="utf-8").strip()
    )
    if len(value) < 32:
        raise ValueError("INTERNAL_API_KEY must contain at least 32 characters")
    app.config["INTERNAL_API_KEY"] = value


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
    role = request.headers.get("X-User-Role", "")
    user_id = request.headers.get("X-User-Id", "")
    if not re.fullmatch(r"[a-zA-Z0-9_-]{1,64}", user_id):
        raise BusinessError("FORBIDDEN", "Identidad interna inválida", 403)
    if role == "ADMIN":
        return
    if (role, user_id, request.method, request.path) == (
        "SERVICE",
        "orders-service",
        "POST",
        "/api/v1/inventories/deductions",
    ):
        return
    raise BusinessError("FORBIDDEN", "No tienes permiso para esta operación", 403)
