# Tema: la concatenación repetida dificulta leer la construcción del mensaje.
def describe_products(products: list[str]) -> str:
    result = ""
    for product in products:
        if result:
            result += ", "
        result += product
    return "Products: " + result

if __name__ == "__main__":
    print(describe_products(["Coffee", "Tea"]))
