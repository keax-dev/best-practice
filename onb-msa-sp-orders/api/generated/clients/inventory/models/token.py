# Generado desde OpenAPI. No editar; ejecutar scripts/generate_apis.py.
from dataclasses import dataclass

from marshmallow import RAISE, Schema, fields, post_load, validate


@dataclass(frozen=True, kw_only=True)
class Token:
    access_token: str
    token_type: str
    expires_in: int


class TokenSchema(Schema):
    class Meta:
        unknown = RAISE

    access_token = fields.String(
        required=True, allow_none=False, validate=[validate.Length(min=1)]
    )
    token_type = fields.String(
        required=True, allow_none=False, validate=[validate.OneOf(["Bearer"])]
    )
    expires_in = fields.Integer(
        required=True, allow_none=False, strict=True, validate=[validate.Range(min=1)]
    )

    @post_load
    def make_model(self, data: dict, **kwargs) -> Token:
        return Token(**data)
