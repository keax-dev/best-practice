# Tema: renombrar un campo rompe al consumidor existente.
def provider() -> dict[str, object]:
    return {"order_id": "order-1", "state": "CREATED"}

def old_client(payload: dict[str, object]) -> str:
    return str(payload["status"])

if __name__ == "__main__":
    try:
        print(old_client(provider()))
    except KeyError as error:
        print(f"Breaking change: {error}")
