# Tema: validar el login y serializar el token según el contrato.
from marshmallow import Schema, fields, validate


class LoginSchema(Schema):
    username = fields.String(required=True, validate=validate.Length(min=1, max=64))
    password = fields.String(required=True, validate=validate.Length(min=1, max=128))


class TokenSchema(Schema):
    access_token = fields.String(required=True, validate=validate.Length(min=1))
    token_type = fields.String(required=True, validate=validate.OneOf(["Bearer"]))
    expires_in = fields.Integer(
        required=True, strict=True, validate=validate.Range(min=1)
    )
