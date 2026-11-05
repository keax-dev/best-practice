# Tema: verificar contratos y detectar diferencias entre servicios y gateway.
from copy import deepcopy
from pathlib import Path

import pytest
import requests
import yaml
from openapi_core import OpenAPI
from openapi_core.contrib.requests import (
    RequestsOpenAPIRequest,
    RequestsOpenAPIResponse,
)

ROOT = Path(__file__).resolve().parents[1]
FOLDERS = ["api-gateway", "onb-msa-sp-orders", "onb-msa-sp-inventories"]


def document(folder: str) -> dict:
    return yaml.safe_load(
        (ROOT / folder / "contracts/openapi.yaml").read_text(encoding="utf-8")
    )


@pytest.mark.parametrize("folder", FOLDERS)
def test_documents_references_requests_and_response_examples(folder):
    contract = OpenAPI.from_file_path(str(ROOT / folder / "contracts/openapi.yaml"))
    spec = document(folder)
    operation_ids = []
    for path, methods in spec["paths"].items():
        for method, operation in methods.items():
            operation_ids.append(operation["operationId"])
            url = spec["servers"][0]["url"] + path
            for parameter in operation.get("parameters", []):
                url = url.replace(
                    "{" + parameter["name"] + "}", str(parameter["example"])
                )
            body = (
                operation.get("requestBody", {})
                .get("content", {})
                .get("application/json", {})
                .get("example")
            )
            prepared = requests.Request(method.upper(), url, json=body).prepare()
            operation_request = RequestsOpenAPIRequest(prepared)
            contract.validate_request(operation_request)
            for status, response in operation["responses"].items():
                import json

                example = response["content"]["application/json"]["example"]
                actual = requests.Response()
                actual.status_code = int(status)
                actual._content = json.dumps(example).encode()
                actual.headers["Content-Type"] = "application/json"
                contract.validate_response(
                    operation_request, RequestsOpenAPIResponse(actual)
                )
    assert len(operation_ids) == len(set(operation_ids))


@pytest.mark.parametrize("folder", FOLDERS[1:])
def test_gateway_operations_and_schemas_match_service(folder):
    gateway = document("api-gateway")
    service = document(folder)
    for name, schema in service["components"]["schemas"].items():
        assert gateway["components"]["schemas"][name] == schema
    for path, methods in service["paths"].items():
        if path == "/health":
            continue
        for method, operation in methods.items():
            published = deepcopy(gateway["paths"][path][method])
            assert set(published["responses"]) - set(operation["responses"]) == {
                "502",
                "504",
            }
            published["responses"].pop("502")
            published["responses"].pop("504")
            assert published == operation
