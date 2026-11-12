# Tema: publicar todo el payload también publica datos sensibles simulados.
import json

if __name__ == "__main__":
    payload = {"order_id": "order-1", "token": "demo-only", "email": "demo@example.com"}
    print(json.dumps(payload))
