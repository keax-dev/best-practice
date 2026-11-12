# Tema: conservar el campo acordado permite seguir atendiendo al consumidor anterior.
def provider() -> dict[str, object]:
    return {"order_id": "order-1", "status": "CREATED", "reason": None}


def old_client(payload: dict[str, object]) -> str:
    return str(payload["status"])


if __name__ == "__main__":
    print(old_client(provider()))
