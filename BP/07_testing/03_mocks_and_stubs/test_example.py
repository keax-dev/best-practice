# Tema: controlar una dependencia y comprobar una interacción con significado.
from unittest.mock import Mock


def test_available_stock_allows_order(load_example):
    module = load_example(__file__)
    lookup = Mock(return_value=3)
    assert module.can_order(1, 2, lookup) is True
    lookup.assert_called_once_with(1)


def test_insufficient_stock_rejects_order(load_example):
    module = load_example(__file__)
    assert module.can_order(1, 4, Mock(return_value=3)) is False
