# Generado desde OpenAPI. No editar; ejecutar scripts/generate_apis.py.
from dataclasses import dataclass

from marshmallow import RAISE, Schema, fields, post_load, validate


@dataclass(frozen=True, kw_only=True)
class Error:
    code: str
    message: str
    details: dict[str, object]


class ErrorSchema(Schema):
    class Meta:
        unknown = RAISE

    code = fields.String(
        required=True,
        allow_none=False,
        validate=[
            validate.OneOf(
                [
                    "INVALID_INPUT",
                    "PRODUCT_NOT_FOUND",
                    "ORDER_NOT_FOUND",
                    "INSUFFICIENT_STOCK",
                    "IDEMPOTENCY_CONFLICT",
                    "SERVICE_UNAVAILABLE",
                    "UPSTREAM_TIMEOUT",
                    "INVALID_RESPONSE",
                    "INTERNAL_ERROR",
                    "UNSUPPORTED_MEDIA_TYPE",
                    "NOT_FOUND",
                    "METHOD_NOT_ALLOWED",
                    "AUTH_REQUIRED",
                    "INVALID_TOKEN",
                    "TOKEN_EXPIRED",
                    "INVALID_CREDENTIALS",
                    "FORBIDDEN",
                ]
            )
        ],
    )
    message = fields.String(required=True, allow_none=False, validate=[])
    details = fields.Dict(required=True, allow_none=False, validate=[])

    @post_load
    def make_model(self, data: dict, **kwargs) -> Error:
        return Error(**data)
