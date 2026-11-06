# Tema: ensamblar un servicio que firma tokens y mantiene usuarios locales.
from pathlib import Path

from config import load_config
from flask import Flask

from api.contract import configure_contract
from api.repositories.user import UserRepository
from api.routes.auth import blueprint
from api.seed import USERS
from api.services.auth import AuthService


def create_app(settings: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config.update(load_config())
    app.config.update(settings or {})
    private_key = app.config.get("JWT_PRIVATE_KEY") or Path(
        app.config["JWT_PRIVATE_KEY_FILE"]
    ).read_text(encoding="utf-8")
    lifetime = int(app.config["JWT_ACCESS_TTL"])
    if lifetime <= 0:
        raise ValueError("JWT_ACCESS_TTL must be positive")
    app.extensions["auth_service"] = AuthService(
        UserRepository(USERS),
        private_key,
        app.config["JWT_ISSUER"],
        app.config["JWT_AUDIENCE"],
        lifetime,
    )
    configure_contract(app)
    app.register_blueprint(blueprint)
    return app
