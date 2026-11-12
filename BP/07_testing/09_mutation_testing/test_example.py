# Tema: demostrar un mutante superviviente y su detección con el caso del umbral.
def test_boundary_case_kills_mutant(load_example):
    module = load_example(__file__)
    assert module.kills_mutant([(80, 80), (120, 110)]) is False
    cases = [(80, 80), (100, 90), (120, 110)]
    assert all(module.original(value) == expected for value, expected in cases)
    assert module.kills_mutant(cases) is True
