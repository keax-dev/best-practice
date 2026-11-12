# Tema: cada modalidad de envío nueva obliga a editar el cálculo existente.
def shipping_cost(method: str) -> int:
    if method == "standard":
        return 5
    if method == "express":
        return 12
    if method == "pickup":
        return 0
    raise ValueError("Unknown shipping method")


def main() -> None:
    for method in ("standard", "express", "pickup"):
        print(f"{method}: {shipping_cost(method)} credits")


if __name__ == "__main__":
    main()
