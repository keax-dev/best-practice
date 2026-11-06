# Tema: validar solicitudes y respuestas con el contrato OpenAPI.
from pathlib import Path

from flask import (
    Blueprint,
    Flask,
    Response,
    current_app,
    make_response,
    request,
    send_file,
)
from flask.typing import ResponseReturnValue
from flask.views import MethodView
from marshmallow import ValidationError
from openapi_core import OpenAPI
from openapi_core.contrib.flask import FlaskOpenAPIRequest, FlaskOpenAPIResponse
from openapi_core.exceptions import OpenAPIError
from werkzeug.exceptions import HTTPException

from api.errors import BusinessError
from api.generated.models.error import Error, ErrorSchema
from api.security import authorize_request


def error_response(
    code: str, message: str, status: int, details: dict | None = None
) -> ResponseReturnValue:
    return make_response(
        ErrorSchema().dump(Error(code=code, message=message, details=details or {})),
        status,
    )


def http_error(error: HTTPException) -> ResponseReturnValue:
    code = {
        400: "INVALID_INPUT",
        404: "NOT_FOUND",
        405: "METHOD_NOT_ALLOWED",
        415: "UNSUPPORTED_MEDIA_TYPE",
    }.get(error.code, "INTERNAL_ERROR")
    message = {
        400: "Solicitud inválida",
        404: "Recurso inexistente",
        405: "Método no permitido",
        415: "Se requiere application/json",
    }.get(error.code, "Error interno")
    return error_response(code, message, error.code or 500)


def unexpected_error(error: Exception) -> ResponseReturnValue:
    current_app.logger.exception("Error interno no controlado", exc_info=error)
    return error_response("INTERNAL_ERROR", "Error interno", 500)


class ContractView(MethodView):
    # Flask sigue creando la vista mediante as_view(); aquí se envuelve su ejecución.
    def dispatch_request(self, **kwargs) -> ResponseReturnValue:
        contract = current_app.extensions["openapi"]
        operation_request = FlaskOpenAPIRequest(request)
        try:
            authorize_request()
        except BusinessError as error:
            response = error_response(
                error.code, error.message, error.status, error.details
            )
            if (
                error.status == 401
                and current_app.config["SERVICE_NAME"] == "api-gateway"
            ):
                response.headers["WWW-Authenticate"] = "Bearer"
            return self._checked(operation_request, response)
        try:
            if request.method == "POST":
                if not request.is_json:
                    return self._checked(
                        operation_request,
                        error_response(
                            "UNSUPPORTED_MEDIA_TYPE",
                            "Se requiere application/json",
                            415,
                        ),
                    )
                request.get_json()  # Detectar JSON malformado antes de cualquier efecto.
            contract.validate_request(operation_request)
        except (OpenAPIError, HTTPException):
            return self._checked(
                operation_request,
                error_response(
                    "INVALID_INPUT", "La solicitud no cumple el contrato", 400
                ),
            )
        try:
            response = make_response(super().dispatch_request(**kwargs))
        except BusinessError as error:
            response = error_response(
                error.code, error.message, error.status, error.details
            )
        except ValidationError:
            response = error_response(
                "INVALID_INPUT", "La solicitud no cumple el contrato", 400
            )
        except HTTPException as error:
            response = http_error(error)
        except Exception:
            current_app.logger.exception("Error interno al ejecutar la operación")
            response = error_response("INTERNAL_ERROR", "Error interno", 500)
        return self._checked(operation_request, response)

    def _checked(
        self, operation_request: FlaskOpenAPIRequest, response: Response
    ) -> ResponseReturnValue:
        try:
            current_app.extensions["openapi"].validate_response(
                operation_request, FlaskOpenAPIResponse(response)
            )
        except Exception:
            current_app.logger.exception("Respuesta fuera del contrato OpenAPI")
            if (
                current_app.config["SERVICE_NAME"] == "api-gateway"
                and request.path != "/health"
            ):
                return error_response(
                    "INVALID_RESPONSE", "Respuesta inválida del servicio", 502
                )
            return error_response("INTERNAL_ERROR", "Respuesta interna inválida", 500)
        return response


def configure_contract(app: Flask) -> None:
    path = Path(app.root_path).parent / "contracts" / "openapi.yaml"
    app.extensions["openapi"] = OpenAPI.from_file_path(str(path))
    app.register_error_handler(HTTPException, http_error)
    app.register_error_handler(Exception, unexpected_error)
    common = Blueprint("common", __name__)

    @common.get("/openapi.yaml")
    def openapi_document() -> ResponseReturnValue:
        return send_file(path, mimetype="application/yaml")

    @common.get("/docs")
    def docs() -> str:
        return """<!doctype html><html lang="es"><head><meta charset="utf-8">
<title>Documentación de la API</title>
<link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5.31.0/swagger-ui.css">
</head><body><div id="swagger-ui"></div>
<script src="https://unpkg.com/swagger-ui-dist@5.31.0/swagger-ui-bundle.js"></script>
<script>SwaggerUIBundle({url: '/openapi.yaml', dom_id: '#swagger-ui'});</script>
</body></html>"""

    app.register_blueprint(common)
