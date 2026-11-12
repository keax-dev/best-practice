# Tema: el mismo except confunde un fallo interno con una entrada inválida.
def apply_policy(quantity: int) -> int:
    raise ValueError("Missing pricing policy")

def process(raw: str) -> str:
    try:
        return str(apply_policy(int(raw)))
    except ValueError:
        return "Invalid quantity"

if __name__ == "__main__":
    print(process("2"))
