# Tema: nombres abreviados ocultan que se está calculando el saldo de un pedido.
def calc(p: int, q: int, d: int) -> int:
    return p * q - d


def main() -> None:
    p = 25
    q = 4
    d = 10
    print(f"Order total: {calc(p, q, d)} credits")


if __name__ == "__main__":
    main()
