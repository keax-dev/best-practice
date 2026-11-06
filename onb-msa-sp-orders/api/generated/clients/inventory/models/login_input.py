# Generado desde OpenAPI. No editar; ejecutar scripts/generate_apis.py.
from dataclasses import dataclass

from marshmallow import RAISE, Schema, fields, post_load, validate


@dataclass(frozen=True, kw_only=True)
class LoginInput:
    username: str
    password: str


class LoginInputSchema(Schema):
    class Meta:
        unknown = RAISE

    username = fields.String(
        required=True,
        allow_none=False,
        validate=[validate.Length(min=1), validate.Length(max=64)],
    )
    password = fields.String(
        required=True,
        allow_none=False,
        validate=[validate.Length(min=1), validate.Length(max=128)],
    )

    @post_load
    def make_model(self, data: dict, **kwargs) -> LoginInput:
        return LoginInput(**data)
