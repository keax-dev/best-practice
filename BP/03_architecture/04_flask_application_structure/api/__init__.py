# Tema: la fábrica compone dependencias una vez por instancia de aplicación.
from flask import Flask

from api.repository import OrderRepository
from api.routes import routes
from api.service import OrderService


def create_app() -> Flask:
    app = Flask(__name__)
    app.extensions["orders"] = OrderService(OrderRepository())
    app.register_blueprint(routes)
    return app
