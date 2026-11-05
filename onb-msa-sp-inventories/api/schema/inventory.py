# Tema: transformar solicitudes y serializar modelos con Marshmallow.
from marshmallow import Schema, fields, validate


class ProductSchema(Schema):
    id = fields.Integer(required=True, strict=True, validate=validate.Range(min=1))
    name = fields.String(required=True)
    stock = fields.Integer(required=True, strict=True, validate=validate.Range(min=0))


class DeductionInputSchema(Schema):
    order_id = fields.UUID(required=True)
    product_id = fields.Integer(
        required=True, strict=True, validate=validate.Range(min=1)
    )
    quantity = fields.Integer(
        required=True, strict=True, validate=validate.Range(min=1)
    )


class DeductionSchema(DeductionInputSchema):
    remaining_stock = fields.Integer(
        required=True, strict=True, validate=validate.Range(min=0)
    )
