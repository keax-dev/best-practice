# Tema: gateway independiente que solo valida y reenvía HTTP.
from config import load_config
from flask import Flask

from api.clients.proxy import ProxyHTTPClient
from api.contract import configure_contract
from api.generated.routes import register_routes
from api.routes.proxy import GatewayAPIImpl
from api.security import configure_security


def create_app(settings: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config.update(load_config())
    app.config.update(settings or {})
    configure_security(app)
    app.extensions["proxy_client"] = ProxyHTTPClient(
        {
            "orders": app.config["ORDERS_SERVICE_URL"],
            "inventories": app.config["INVENTORIES_SERVICE_URL"],
            "auth": app.config["AUTH_SERVICE_URL"],
        },
        app.config["CONNECT_TIMEOUT"],
        app.config["ORDERS_TIMEOUT"],
        app.config["INVENTORIES_TIMEOUT"],
        app.config["AUTH_TIMEOUT"],
    )
    configure_contract(app)
    implementation = GatewayAPIImpl(
        app.extensions["proxy_client"], app.config["SERVICE_NAME"]
    )
    app.extensions["gateway_api"] = implementation
    register_routes(app, implementation)
    return app
