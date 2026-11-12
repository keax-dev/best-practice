# Tema: preparar, ejecutar y comprobar un resultado esperado.
def test_total_two_units_returns_ten(load_example):
    module = load_example(__file__)
    unit_price, quantity = 5, 2
    actual = module.total(unit_price, quantity)
    assert actual == 10
