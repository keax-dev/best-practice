# Tema: ensamblar dependencias una sola vez por instancia de aplicación.
from config import load_config
from flask import Flask

from api.clients.inventory import InventoryHTTPClient
from api.contract import configure_contract
from api.repositories.order import OrderRepository
from api.routes.order import blueprint
from api.services.order import OrderService


def create_app(settings: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config.update(load_config())
    app.config.update(settings or {})
    repository = OrderRepository()
    client = InventoryHTTPClient(
        app.config["API_GATEWAY_URL"],
        (app.config["CONNECT_TIMEOUT"], app.config["VALIDATION_TIMEOUT"]),
    )
    app.extensions["order_repository"] = repository
    app.extensions["order_service"] = OrderService(repository, client)
    configure_contract(app)
    app.register_blueprint(blueprint)
    return app
