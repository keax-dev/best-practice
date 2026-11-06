# Generado desde OpenAPI. No editar; ejecutar scripts/generate_apis.py.
from dataclasses import dataclass

from marshmallow import RAISE, Schema, fields, post_load, validate


@dataclass(frozen=True, kw_only=True)
class Health:
    status: str
    service: str


class HealthSchema(Schema):
    class Meta:
        unknown = RAISE

    status = fields.String(
        required=True, allow_none=False, validate=[validate.OneOf(["ok"])]
    )
    service = fields.String(required=True, allow_none=False, validate=[])

    @post_load
    def make_model(self, data: dict, **kwargs) -> Health:
        return Health(**data)
