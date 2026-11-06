# Generado desde OpenAPI. No editar; ejecutar scripts/generate_apis.py.
from dataclasses import dataclass
from uuid import UUID

from marshmallow import RAISE, Schema, fields, post_load, validate


@dataclass(frozen=True, kw_only=True)
class DeductionInput:
    order_id: UUID
    product_id: int
    quantity: int


class DeductionInputSchema(Schema):
    class Meta:
        unknown = RAISE

    order_id = fields.UUID(required=True, allow_none=False, validate=[])
    product_id = fields.Integer(
        required=True, allow_none=False, strict=True, validate=[validate.Range(min=1)]
    )
    quantity = fields.Integer(
        required=True, allow_none=False, strict=True, validate=[validate.Range(min=1)]
    )

    @post_load
    def make_model(self, data: dict, **kwargs) -> DeductionInput:
        return DeductionInput(**data)
