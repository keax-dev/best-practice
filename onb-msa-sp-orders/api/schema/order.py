# Tema: contrato de entrada y representación JSON del pedido.
from marshmallow import Schema, fields, validate


class OrderInputSchema(Schema):
    product_id = fields.Integer(
        required=True, strict=True, validate=validate.Range(min=1)
    )
    quantity = fields.Integer(
        required=True, strict=True, validate=validate.Range(min=1)
    )


class OrderSchema(OrderInputSchema):
    id = fields.UUID(required=True)
    user_id = fields.String(
        required=True, validate=validate.Regexp(r"^[a-zA-Z0-9_-]{1,64}$")
    )
    status = fields.String(
        required=True,
        validate=validate.OneOf(
            ["CREADO", "CONFIRMADO", "RECHAZADO", "ERROR_VALIDACION"]
        ),
    )
    reason = fields.String(required=True, allow_none=True)
    created_at = fields.DateTime(required=True, format="%Y-%m-%dT%H:%M:%S.%fZ")


class DeductionSchema(Schema):
    order_id = fields.UUID(required=True)
    product_id = fields.Integer(
        required=True, strict=True, validate=validate.Range(min=1)
    )
    quantity = fields.Integer(
        required=True, strict=True, validate=validate.Range(min=1)
    )
    remaining_stock = fields.Integer(
        required=True, strict=True, validate=validate.Range(min=0)
    )


class ErrorSchema(Schema):
    code = fields.String(required=True)
    message = fields.String(required=True)
    details = fields.Dict(required=True)
