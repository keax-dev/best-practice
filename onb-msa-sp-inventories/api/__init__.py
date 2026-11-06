# Tema: construir una aplicación con memoria nueva en cada instancia.
from config import load_config
from flask import Flask

from api.contract import configure_contract
from api.generated.routes import register_routes
from api.repositories.inventory import InventoryRepository
from api.routes.inventory import InventoryAPIImpl
from api.security import configure_security
from api.seed import INITIAL_PRODUCTS
from api.services.inventory import InventoryService


def create_app(settings: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config.update(load_config())
    app.config.update(settings or {})
    configure_security(app)
    repository = InventoryRepository(INITIAL_PRODUCTS)
    app.extensions["inventory_repository"] = repository
    app.extensions["inventory_service"] = InventoryService(repository)
    configure_contract(app)
    implementation = InventoryAPIImpl(
        app.extensions["inventory_service"], app.config["SERVICE_NAME"]
    )
    app.extensions["inventories_api"] = implementation
    register_routes(app, implementation)
    return app
