# Tema: crear una aplicación Flask e inspeccionar su respuesta sin abrir un servidor.
from api import create_app

if __name__ == "__main__":
    with create_app().test_client() as client:
        response = client.post("/orders", json={"quantity": 2})
        print(response.status_code, response.get_json())
