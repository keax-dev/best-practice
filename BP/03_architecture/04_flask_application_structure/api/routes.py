# Tema: Blueprint y MethodView traducen HTTP hacia el servicio.
from dataclasses import asdict

from flask import Blueprint, current_app, jsonify, request
from flask.views import MethodView

routes = Blueprint("orders", __name__)


class OrdersAPI(MethodView):
    def get(self):
        orders = current_app.extensions["orders"].repository.list_all()
        return jsonify([asdict(order) for order in orders])

    def post(self):
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict) or set(payload) != {"quantity"}:
            return jsonify(code="INVALID_INPUT"), 400
        try:
            order = current_app.extensions["orders"].create(payload["quantity"])
        except ValueError:
            return jsonify(code="INVALID_QUANTITY"), 400
        except OverflowError:
            return jsonify(code="DEMO_CAPACITY_REACHED"), 409
        return jsonify(asdict(order)), 201


routes.add_url_rule("/orders", view_func=OrdersAPI.as_view("orders"))
