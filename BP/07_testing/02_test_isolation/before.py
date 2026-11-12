# Tema: el estado global persiste entre operaciones de una misma sesión.
orders: list[str] = []

def add_order(order_id: str) -> list[str]:
    orders.append(order_id)
    return orders

if __name__ == "__main__":
    print(add_order("order-1"))
    print(add_order("order-2"))
