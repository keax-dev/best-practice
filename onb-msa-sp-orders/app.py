# Tema: punto de entrada del servidor local con hilos y sin recarga.
from api import create_app

if __name__ == "__main__":
    app = create_app()
    try:
        app.run(
            host="127.0.0.1", port=5001, threaded=True, use_reloader=False, debug=False
        )
    finally:
        # Al detener normalmente el servidor, esperar a las validaciones ya aceptadas.
        app.extensions["validation_executor"].shutdown(wait=True)
