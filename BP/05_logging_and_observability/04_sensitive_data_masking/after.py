# Tema: una lista permitida excluye datos sensibles incluso en estructuras anidadas.
import json


def safe_event(payload: dict[str, object]) -> dict[str, str]:
    order_id = payload.get("order_id")
    if not isinstance(order_id, str) or not order_id.startswith("order-"):
        raise ValueError("Expected a synthetic order identifier")
    return {"event": "order_received", "order_id": order_id}


if __name__ == "__main__":
    payload = {"order_id": "order-1", "token": "demo-only", "customer": {"email": "demo@example.com"}}
    print(json.dumps(safe_event(payload)))
