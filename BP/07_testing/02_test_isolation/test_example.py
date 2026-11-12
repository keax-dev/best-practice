# Tema: el estado y las colecciones devueltas no se comparten entre repositorios.
def test_repositories_do_not_share_orders(load_example):
    module = load_example(__file__)
    first, second = module.OrderRepository(), module.OrderRepository()
    first.add("order-1")
    returned = first.list_all()
    returned.clear()
    assert second.list_all() == []
    assert first.list_all() == ["order-1"]
