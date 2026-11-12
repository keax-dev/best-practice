# Tema: un valor fijo obliga a editar código para cambiar el entorno.
def read_timeout() -> float:
    return 2.0

if __name__ == "__main__":
    print(f"Timeout: {read_timeout()}")
