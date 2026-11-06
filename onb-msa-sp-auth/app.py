# Tema: ejecutar Autenticación como un proceso independiente.
from api import create_app

if __name__ == "__main__":
    create_app().run(
        host="127.0.0.1", port=5003, threaded=True, use_reloader=False, debug=False
    )
