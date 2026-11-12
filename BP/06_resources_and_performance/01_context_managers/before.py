# Tema: abrir un recurso sin un bloque de contexto obliga a recordar su cierre.
from tempfile import TemporaryFile

if __name__ == "__main__":
    file = TemporaryFile(mode="w+t", encoding="utf-8")
    file.write("Coffee")
    print(f"Closed before cleanup: {file.closed}")
    file.close()
