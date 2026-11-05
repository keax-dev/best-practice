# Tema: registros iniciales; cada aplicación obtiene su propia copia.
from api.models.product import Product

INITIAL_PRODUCTS = (
    Product(id=1, name="Café", stock=10),
    Product(id=2, name="Té", stock=5),
    Product(id=3, name="Chocolate", stock=0),
)
