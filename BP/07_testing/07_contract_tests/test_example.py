# Tema: verificar el acuerdo de entrada con mensajes válidos y no válidos.
import pytest


@pytest.mark.parametrize(
    "payload,expected",
    [
        ({"quantity": 2}, True),
        ({"quantity": 0}, False),
        ({"quantity": True}, False),
        ({"quantity": 1, "user_id": "other"}, False),
        ({}, False),
    ],
)
def test_message_contract(load_example, payload, expected):
    validator = load_example(__file__, filename="example.py").contract_validator()
    assert validator.is_valid(payload) is expected
