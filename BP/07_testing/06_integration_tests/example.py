# Tema: una aplicación mínima permite probar rutas y estado por instancia.
from flask import Flask, jsonify, request


def create_app() -> Flask:
    app = Flask(__name__)
    orders: list[dict[str, int]] = []

    @app.post("/orders")
    def create_order():
        body = request.get_json(silent=True)
        quantity = body.get("quantity") if isinstance(body, dict) else None
        if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity <= 0:
            return jsonify(code="INVALID_QUANTITY"), 400
        order = {"quantity": quantity}
        orders.append(order)
        return jsonify(order), 201

    @app.get("/orders")
    def list_orders():
        return jsonify(orders)

    return app


if __name__ == "__main__":
    with create_app().test_client() as client:
        response = client.post("/orders", json={"quantity": 2})
        print(response.status_code, response.get_json())
