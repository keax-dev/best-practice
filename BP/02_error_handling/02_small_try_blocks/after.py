# Tema: un try pequeño no cambia la interpretación de fallos posteriores.
def apply_policy(quantity: int) -> int:
    raise ValueError("Missing pricing policy")


def process(raw: str) -> str:
    try:
        quantity = int(raw)
    except ValueError:
        return "Invalid quantity"
    return str(apply_policy(quantity))


if __name__ == "__main__":
    try:
        print(process("2"))
    except ValueError as error:
        print(f"Configuration error: {error}")
