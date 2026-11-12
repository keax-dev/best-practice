# Tema: probar el recorrido HTTP y efectos del negocio con instancias nuevas.
def test_http_creation_and_isolation(load_example):
    module = load_example(__file__, filename="example.py")
    with module.create_app().test_client() as client:
        assert client.post("/orders", json={"quantity": True}).status_code == 400
        assert client.get("/orders").get_json() == []
        assert client.post("/orders", json={"quantity": 2}).status_code == 201
        assert client.get("/orders").get_json() == [{"quantity": 2}]
    with module.create_app().test_client() as client:
        assert client.get("/orders").get_json() == []
