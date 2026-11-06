# Tema: generar modelos, esquemas, interfaces, rutas y clientes desde los contratos.
import argparse
import hashlib
import importlib.resources
import json
import re
import shutil
import subprocess
import sys
import tempfile
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

import yaml
from openapi_core import OpenAPI

ROOT = Path(__file__).resolve().parents[1]
APPS = {
    "auth": "onb-msa-sp-auth",
    "orders": "onb-msa-sp-orders",
    "inventories": "onb-msa-sp-inventories",
    "gateway": "api-gateway",
}
TEMPLATES = ROOT / "codegen/templates"
HEADER = "# Generado desde OpenAPI. No editar; ejecutar scripts/generate_apis.py."


def python_field(
    schema: dict, required: bool = True, transport: bool = False
) -> tuple[str, str]:
    kind, format_name = schema.get("type"), schema.get("format")
    field_type, python_type = {
        "string": ("fields.String", "str"),
        "integer": ("fields.Integer", "int"),
        "object": ("fields.Dict", "dict[str, object]"),
        "boolean": ("fields.Boolean", "bool"),
    }[kind]
    if kind == "object" and schema.get("additionalProperties") is not True:
        raise ValueError("Only free-form dictionary properties are supported")
    if format_name:
        if (kind, format_name) == ("string", "uuid"):
            field_type, python_type = "fields.UUID", "UUID"
        elif (kind, format_name) == ("string", "date-time"):
            field_type, python_type = "UTCDateTime", "datetime"
        else:
            raise ValueError(f"Unsupported format: {format_name}")
    arguments = [
        f"required={required!r}",
        f"allow_none={schema.get('nullable', False)!r}",
    ]
    if kind == "integer":
        arguments.append(f"strict={not transport!r}")
    validators = []
    for key, argument in (("minLength", "min"), ("maxLength", "max")):
        if key in schema:
            validators.append(f"validate.Length({argument}={schema[key]!r})")
    for key, argument in (("minimum", "min"), ("maximum", "max")):
        if key in schema:
            validators.append(f"validate.Range({argument}={schema[key]!r})")
    if "enum" in schema:
        validators.append(f"validate.OneOf({schema['enum']!r})")
    if "pattern" in schema:
        if format_name == "date-time":
            arguments.append(f"pattern={schema['pattern']!r}")
        else:
            validators.append(f"validate.Regexp({schema['pattern']!r})")
    arguments.append("validate=[" + ", ".join(validators) + "]")
    if schema.get("nullable"):
        python_type += " | None"
    return python_type, field_type + "(" + ", ".join(arguments) + ")"


def prepared_contract(path: Path, selected: list[str] | None = None) -> dict:
    OpenAPI.from_file_path(str(path))
    document = yaml.safe_load(path.read_text(encoding="utf-8"))
    schemas = document["components"]["schemas"]
    for name, schema in schemas.items():
        if (
            schema.get("type") != "object"
            or schema.get("additionalProperties") is not False
        ):
            raise ValueError(f"{name}: DTOs must be closed objects")
        if set(schema.get("required", [])) != set(schema.get("properties", {})):
            raise ValueError(f"{name}: templates currently require all DTO properties")
        for prop in schema["properties"].values():
            allowed = {
                "type",
                "format",
                "enum",
                "minimum",
                "maximum",
                "minLength",
                "maxLength",
                "pattern",
                "description",
                "example",
                "nullable",
                "additionalProperties",
            }
            if {key for key in prop if not key.startswith("x-")} - allowed:
                raise ValueError(
                    f"{name}: extend templates before using these property constraints"
                )
            prop["x-python-type"], prop["x-python-field"] = python_field(prop)
    filtered = {}
    for route, methods in document["paths"].items():
        for method, operation in methods.items():
            if selected and operation["operationId"] not in selected:
                continue
            if method not in {"get", "post"} or operation.get("tags"):
                raise ValueError(
                    "Templates support one untagged GET/POST API per application"
                )
            if not re.fullmatch(r"[A-Za-z][A-Za-z0-9]*", operation["operationId"]):
                raise ValueError("Use alphanumeric operationId values")
            if "requestBody" in operation:
                body = operation["requestBody"]
                if (
                    not body.get("required")
                    or set(body["content"]) != {"application/json"}
                    or "$ref" not in body["content"]["application/json"]["schema"]
                ):
                    raise ValueError(
                        "Request bodies must be required, referenced JSON DTOs"
                    )
            for parameter in operation.get("parameters", []):
                if not parameter.get("required") or parameter["in"] not in {
                    "path",
                    "header",
                    "query",
                }:
                    raise ValueError(
                        "Templates support required path/header/query parameters"
                    )
                parameter["x-python-type"], parameter["x-python-field"] = python_field(
                    parameter["schema"], transport=True
                )
                if parameter["in"] == "path":
                    if not re.fullmatch(r"[a-z_][a-z0-9_]*", parameter["name"]):
                        raise ValueError("Use snake_case path parameter names")
                    source = parameter["name"]
                else:
                    source = f"request.{'headers' if parameter['in'] == 'header' else 'args'}.get({parameter['name']!r})"
                parameter["x-python-source"] = source
            successes = [
                (code, response)
                for code, response in operation["responses"].items()
                if code.startswith("2")
            ]
            if len(successes) != 1:
                raise ValueError("Each operation must declare one successful response")
            code, response = successes[0]
            if set(response["content"]) != {"application/json"}:
                raise ValueError("Successful responses must use JSON")
            result_schema = response["content"]["application/json"]["schema"]
            many = result_schema.get("type") == "array"
            result_ref = result_schema.get("items", {}) if many else result_schema
            if "$ref" not in result_ref:
                raise ValueError(
                    "Successful responses must reference a DTO or an array of DTOs"
                )
            result_type = result_ref["$ref"].rsplit("/", 1)[1]
            operation.update(
                {
                    "x-python-method": method,
                    "x-python-status": code,
                    "x-python-response-type": f"list[{result_type}]"
                    if many
                    else result_type,
                    "x-python-response-schema": result_type
                    + "Schema("
                    + ("many=True" if many else "")
                    + ")",
                }
            )
            filtered.setdefault(route, {})[method] = operation
    if not filtered:
        raise ValueError("No operations selected")
    document["paths"] = filtered
    return document


def run(command: list[str]) -> None:
    result = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)


def compiler() -> list[str]:
    if version("openapi-generator-cli") != "7.27.0" or version("ruff") != "0.17.3":
        raise RuntimeError("Install requirements-codegen.txt for the pinned tools")
    java = shutil.which("java")
    if not java:
        raise RuntimeError("Java is needed for generation, not for running Flask")
    return [
        java,
        "-Dfile.encoding=UTF-8",
        "-jar",
        str(
            importlib.resources.files("openapi_generator_cli") / "openapi-generator.jar"
        ),
    ]


def render_package(
    command: list[str],
    contract: Path,
    config: dict,
    directory: Path,
    client: bool = False,
    operations: list[str] | None = None,
) -> dict[str, bytes]:
    directory.mkdir(parents=True)
    prepared = directory / "openapi.yaml"
    prepared.write_text(
        yaml.safe_dump(
            prepared_contract(contract, operations), sort_keys=False, allow_unicode=True
        ),
        encoding="utf-8",
    )
    config_path = directory / "config.yaml"
    config_path.write_text(yaml.safe_dump(config), encoding="utf-8")
    output = directory / "output"
    run(
        command
        + [
            "generate",
            "-g",
            "python-flask",
            "-i",
            str(prepared),
            "-o",
            str(output),
            "-c",
            str(config_path),
            "-t",
            str(TEMPLATES),
            "--global-property",
            "models,apis,supportingFiles,apiDocs=false,apiTests=false,modelDocs=false,modelTests=false",
        ]
    )
    properties = config["additionalProperties"]
    package = output.joinpath(*properties["packageName"].split("."))
    selected = [package / "__init__.py", package / "models/__init__.py"]
    selected += [
        p
        for p in (package / "models").glob("*.py")
        if p.name not in {"__init__.py", "base_model.py"}
    ]
    if client:
        selected.append(package / "client.py")
    else:
        selected += [
            package / "runtime.py",
            package / "routes.py",
            package / "interfaces/__init__.py",
            package / "interfaces" / (properties["defaultController"] + ".py"),
        ]
    result = {}
    for path in selected:
        text = path.read_text(encoding="utf-8")
        if not text.startswith(HEADER):
            raise ValueError(f"Unexpected generated artifact: {path.name}")
        result[path.relative_to(package).as_posix()] = text.encode()
    return result


def render(app: str, contract: Path, directory: Path) -> dict[str, bytes]:
    config_path = ROOT / APPS[app] / "codegen/config.yaml"
    configuration = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    command = compiler()
    files = render_package(command, contract, configuration, directory / "server")
    sources = {
        "contract": contract.read_bytes(),
        "config": config_path.read_bytes(),
        "generator": Path(__file__).read_bytes(),
    }
    for index, client in enumerate(configuration.get("clients", [])):
        source = ROOT / client["contract"]
        package_name = "api.generated.clients." + client["name"]
        client_config = {
            "additionalProperties": {
                **configuration["additionalProperties"],
                "packageName": package_name,
                "clientClassName": client["className"],
            },
            "files": {
                "client.mustache": {
                    "templateType": "SupportingFiles",
                    "folder": package_name.replace(".", "/"),
                    "destinationFilename": "client.py",
                }
            },
        }
        result = render_package(
            command,
            source,
            client_config,
            directory / f"client-{index}",
            True,
            client["operations"],
        )
        files.update(
            {f"clients/{client['name']}/{name}": data for name, data in result.items()}
        )
        files["clients/__init__.py"] = (HEADER + "\n").encode()
        sources[f"client-{index}"] = source.read_bytes()
    sources.update(
        {p.name: p.read_bytes() for p in sorted(TEMPLATES.glob("*.mustache"))}
    )
    formatted = directory / "formatted"
    for name, data in files.items():
        path = formatted / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    run(
        [
            sys.executable,
            "-m",
            "ruff",
            "check",
            "--isolated",
            "--select",
            "I,F401",
            "--config",
            'lint.isort.known-first-party=["api"]',
            "--fix",
            str(formatted),
        ]
    )
    run([sys.executable, "-m", "ruff", "format", "--isolated", str(formatted)])
    for name in files:
        content = (formatted / name).read_text(encoding="utf-8")
        compile(content, name, "exec")
        files[name] = content.encode()
    digest = hashlib.sha256()
    for name, data in sorted(sources.items()):
        digest.update(
            name.encode()
            + b"\0"
            + data.decode("utf-8").replace("\r\n", "\n").encode()
            + b"\0"
        )
    manifest = {
        "generator": "openapi-generator-cli",
        "version": "7.27.0",
        "application": app,
        "input_sha256": digest.hexdigest(),
        "files": sorted(files),
    }
    files["manifest.json"] = (json.dumps(manifest, indent=2) + "\n").encode()
    return files


def generate(app: str, contract: Path, output: Path, check: bool) -> bool:
    with tempfile.TemporaryDirectory(prefix="coe-codegen-") as directory:
        files = render(app, contract, Path(directory))
    output = output.resolve()
    existing = (
        {p.relative_to(output).as_posix(): p for p in output.rglob("*.py")}
        if output.exists()
        else {}
    )
    extras = set(existing) - set(files)
    changed = {
        name
        for name, data in files.items()
        if not (output / name).is_file()
        or (output / name).read_text(encoding="utf-8").encode() != data
    }
    if check:
        if changed or extras:
            print(
                f"{app}: generated files are stale: "
                + ", ".join(sorted(changed | extras))
            )
            return False
        print(f"{app}: generated files match the contract and templates.")
        return True
    for name in extras:
        path = existing[name].resolve()
        if not path.is_relative_to(output) or not path.read_text(
            encoding="utf-8"
        ).startswith((HEADER, "# Generado desde contracts/openapi.yaml.")):
            raise ValueError("Refusing to remove a file not owned by the generator")
        path.unlink()
    for name, data in files.items():
        path = output / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    print(f"{app}: generated {len(files) - 1} Python files in {output}")
    return True


def main(default_app: str = "all") -> None:
    parser = argparse.ArgumentParser(
        description="Generar las APIs Flask a partir de OpenAPI"
    )
    parser.add_argument("--app", choices=["all", *APPS], default=default_app)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--contract", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.app == "all" and (args.contract or args.output):
        parser.error("--contract/--output require selecting one --app")
    try:
        success = True
        for app in APPS if args.app == "all" else [args.app]:
            root = ROOT / APPS[app]
            success = (
                generate(
                    app,
                    (args.contract or root / "contracts/openapi.yaml").resolve(),
                    (args.output or root / "api/generated").resolve(),
                    args.check,
                )
                and success
            )
    except (OSError, ValueError, KeyError, RuntimeError, PackageNotFoundError) as error:
        parser.exit(1, f"API generation failed: {error}\n")
    if not success:
        parser.exit(1)


if __name__ == "__main__":
    main()
