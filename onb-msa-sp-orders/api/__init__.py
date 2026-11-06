# Tema: ensamblar dependencias una sola vez por instancia de aplicación.
from concurrent.futures import ThreadPoolExecutor

from config import load_config
from flask import Flask

from api.clients.inventory import InventoryHTTPClient
from api.contract import configure_contract
from api.generated.routes import register_routes
from api.repositories.order import OrderRepository
from api.routes.order import OrdersAPIImpl
from api.security import configure_security
from api.services.order import OrderService


def create_app(settings: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config.update(load_config())
    app.config.update(settings or {})
    configure_security(app)
    repository = OrderRepository()
    client = InventoryHTTPClient(
        app.config["API_GATEWAY_URL"],
        (app.config["CONNECT_TIMEOUT"], app.config["VALIDATION_TIMEOUT"]),
        app.config["ORDERS_SERVICE_KEY"],
    )
    app.extensions["order_repository"] = repository
    configure_contract(app)
    executor = ThreadPoolExecutor(
        max_workers=app.config["VALIDATION_WORKERS"],
        thread_name_prefix="order-validation",
    )
    app.extensions["validation_executor"] = executor
    app.extensions["order_service"] = OrderService(repository, client, executor)
    implementation = OrdersAPIImpl(
        app.extensions["order_service"], app.config["SERVICE_NAME"]
    )
    app.extensions["orders_api"] = implementation
    register_routes(app, implementation)
    return app
