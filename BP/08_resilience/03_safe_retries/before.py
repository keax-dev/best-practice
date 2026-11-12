# Tema: repetir cualquier error no distingue fallos temporales de entradas inválidas.
def retry(operation, attempts: int = 3):
    for attempt in range(attempts):
        try:
            return operation()
        except Exception:
            if attempt == attempts - 1:
                raise

if __name__ == "__main__":
    print(retry(lambda: "Catalog response"))
