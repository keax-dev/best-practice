# Tema: una lambda con nombre y un diccionario esconden la estructura del dato.
calculate_total = lambda unit_price, quantity: unit_price * quantity

if __name__ == "__main__":
    order = {"unit_price": 5, "quantity": 2}
    print(calculate_total(order["unit_price"], order["quantity"]))
