# Tema: construir una aplicación con memoria nueva en cada instancia.
from config import load_config
from flask import Flask

from api.contract import configure_contract
from api.repositories.inventory import InventoryRepository
from api.routes.inventory import blueprint
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
    app.register_blueprint(blueprint)
    return app
