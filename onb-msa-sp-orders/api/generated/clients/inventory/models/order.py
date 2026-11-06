# Generado desde OpenAPI. No editar; ejecutar scripts/generate_apis.py.
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from marshmallow import RAISE, Schema, fields, post_load, validate

from api.generated.runtime import UTCDateTime


@dataclass(frozen=True, kw_only=True)
class Order:
    id: UUID
    product_id: int
    quantity: int
    status: str
    reason: str | None
    created_at: datetime
    user_id: str


class OrderSchema(Schema):
    class Meta:
        unknown = RAISE

    id = fields.UUID(required=True, allow_none=False, validate=[])
    product_id = fields.Integer(
        required=True, allow_none=False, strict=True, validate=[validate.Range(min=1)]
    )
    quantity = fields.Integer(
        required=True, allow_none=False, strict=True, validate=[validate.Range(min=1)]
    )
    status = fields.String(
        required=True,
        allow_none=False,
        validate=[
            validate.OneOf(["CREADO", "CONFIRMADO", "RECHAZADO", "ERROR_VALIDACION"])
        ],
    )
    reason = fields.String(required=True, allow_none=True, validate=[])
    created_at = UTCDateTime(
        required=True,
        allow_none=False,
        pattern="^\\d{4}-\\d{2}-\\d{2}T.*Z$",
        validate=[],
    )
    user_id = fields.String(
        required=True,
        allow_none=False,
        validate=[validate.Regexp("^[a-zA-Z0-9_-]{1,64}$")],
    )

    @post_load
    def make_model(self, data: dict, **kwargs) -> Order:
        return Order(**data)
