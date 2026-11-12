# Tema: la tabla de casos produce pruebas independientes.
import pytest


@pytest.mark.parametrize(
    "value,expected", [(2, True), (0, False), (-1, False), (True, False), ("2", False), (None, False)]
)
def test_quantity_validation(load_example, value, expected):
    module = load_example(__file__)
    assert module.is_positive_quantity(value) is expected
