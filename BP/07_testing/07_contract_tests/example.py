# Tema: el contrato externo determina las reglas del mensaje.
import json
from pathlib import Path

from jsonschema import Draft202012Validator


def contract_validator() -> Draft202012Validator:
    schema = json.loads(Path(__file__).with_name("contract.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


if __name__ == "__main__":
    validator = contract_validator()
    for payload in ({"quantity": 2}, {"quantity": True}):
        print(f"{payload}: {validator.is_valid(payload)}")
