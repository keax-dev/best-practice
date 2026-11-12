# Tema: verificar HTTP, validación y aislamiento en la composición real.
def test_application_instances_are_independent(load_example):
    module = load_example(__file__, filename="example.py")
    first, second = module.create_app(), module.create_app()
    with first.test_client() as client:
        assert client.post("/orders", json={"quantity": True}).status_code == 400
        assert client.get("/orders").get_json() == []
        response = client.post("/orders", json={"quantity": 2})
        assert response.status_code == 201
        assert response.get_json()["quantity"] == 2
    with second.test_client() as client:
        assert client.get("/orders").get_json() == []
