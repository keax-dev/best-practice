# Tema: la función depende directamente de la herramienta que consulta el stock.
def check_stock(product_id: int) -> int:
    return 10

def can_order(product_id: int, quantity: int) -> bool:
    return check_stock(product_id) >= quantity

if __name__ == "__main__":
    print(can_order(1, 2))
