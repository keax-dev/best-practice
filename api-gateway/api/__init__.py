# Tema: gateway independiente que solo valida y reenvía HTTP.
from config import load_config
from flask import Flask

from api.clients.proxy import ProxyHTTPClient
from api.contract import configure_contract
from api.routes.proxy import blueprint


def create_app(settings: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config.update(load_config())
    app.config.update(settings or {})
    app.extensions["proxy_client"] = ProxyHTTPClient(
        {
            "orders": app.config["ORDERS_SERVICE_URL"],
            "inventories": app.config["INVENTORIES_SERVICE_URL"],
        },
        app.config["CONNECT_TIMEOUT"],
        app.config["ORDERS_TIMEOUT"],
        app.config["INVENTORIES_TIMEOUT"],
    )
    configure_contract(app)
    app.register_blueprint(blueprint)
    return app
