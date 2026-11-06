# Tema: las rutas registradas deben coincidir con las operaciones del contrato.
import re
from pathlib import Path

import yaml


def test_routes_match_contract(app):
    path = Path(app.root_path).parent / "contracts/openapi.yaml"
    document = yaml.safe_load(path.read_text(encoding="utf-8"))
    expected = {
        (path, method.upper())
        for path, methods in document["paths"].items()
        for method in methods
    }
    actual = set()
    for rule in app.url_map.iter_rules():
        if rule.rule in {"/docs", "/openapi.yaml"} or rule.endpoint == "static":
            continue
        path = re.sub(
            r"<(?:[^:>]+:)?([^>]+)>",
            lambda match: "{" + match.group(1) + "}",
            rule.rule,
        )
        actual.update((path, method) for method in rule.methods - {"HEAD", "OPTIONS"})
    assert actual == expected


def test_health_and_documentation(client):
    assert client.get("/health").status_code == 200
    assert client.get("/openapi.yaml").status_code == 200
    assert "/openapi.yaml" in client.get("/docs").text
