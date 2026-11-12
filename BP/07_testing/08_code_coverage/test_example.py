# Tema: comprobar ambos caminos, no solo ejecutar líneas.
import pytest


@pytest.mark.parametrize("quantity,expected", [(1, "VALID"), (0, "INVALID"), (-1, "INVALID")])
def test_classification(load_example, quantity, expected):
    assert load_example(__file__).classify(quantity) == expected
