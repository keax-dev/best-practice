# Tema: preparar claves sin rotarlas ni sobrescribir una configuración existente.
from scripts.setup_local import prepare


def test_setup_is_repeatable(tmp_path):
    directory = tmp_path / "keys"
    prepare(directory)
    before = {path.name: path.read_bytes() for path in directory.iterdir()}
    prepare(directory)
    assert {path.name: path.read_bytes() for path in directory.iterdir()} == before
    assert set(before) == {
        "jwt-private.pem",
        "jwt-public.pem",
        "internal-api.key",
        "orders-service.key",
    }
