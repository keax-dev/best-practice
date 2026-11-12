# Tema: verificar el umbral y el contrato de error.
import pytest


@pytest.mark.parametrize("total,expected", [(99, 99), (100, 90), (101, 91)])
def test_discount_boundary(load_example, total, expected):
    assert load_example(__file__).discounted_total(total) == expected


def test_negative_total_raises_error(load_example):
    with pytest.raises(ValueError, match="cannot be negative"):
        load_example(__file__).discounted_total(-1)
