# Tema: join reúne elementos y la f-string expresa el mensaje.
def describe_products(products: list[str]) -> str:
    return f"Products: {', '.join(products)}"


if __name__ == "__main__":
    print(describe_products(["Coffee", "Tea"]))
