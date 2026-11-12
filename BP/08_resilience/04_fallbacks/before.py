# Tema: ocultar el error con una lista vacía confunde caída y ausencia de datos.
def get_catalog(fetch) -> list[str]:
    try:
        return fetch()
    except ConnectionError:
        return []

if __name__ == "__main__":
    print(get_catalog(lambda: ["Coffee"]))
