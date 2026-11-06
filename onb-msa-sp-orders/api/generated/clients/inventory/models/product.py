# Generado desde OpenAPI. No editar; ejecutar scripts/generate_apis.py.
from dataclasses import dataclass

from marshmallow import RAISE, Schema, fields, post_load, validate


@dataclass(frozen=True, kw_only=True)
class Product:
    id: int
    name: str
    stock: int


class ProductSchema(Schema):
    class Meta:
        unknown = RAISE

    id = fields.Integer(
        required=True, allow_none=False, strict=True, validate=[validate.Range(min=1)]
    )
    name = fields.String(required=True, allow_none=False, validate=[])
    stock = fields.Integer(
        required=True, allow_none=False, strict=True, validate=[validate.Range(min=0)]
    )

    @post_load
    def make_model(self, data: dict, **kwargs) -> Product:
        return Product(**data)
