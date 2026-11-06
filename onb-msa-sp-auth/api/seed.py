# Tema: dos usuarios de demostración con hashes de contraseña.
from api.models.user import User

USERS = (
    User(
        "user-admin",
        "admin",
        "scrypt:32768:8:1$fzja8Z3LB0V3DVB3$cc44e828e8c2a9b5ca5fe86d2fe23fd138d82a9a6ff2ca214e516e4822c8cb373dab32726f9b5761ac3a5c5aed2298be3f7324d9fb20fb984d854b54b04d696b",
        "ADMIN",
    ),
    User(
        "user-client",
        "client",
        "scrypt:32768:8:1$4zTIQvmr5FPePcoC$d7341ef1a53e77da2bf47b30b94f35c8a9a271f68394c132bd08a3f0b6f9593ed50ac829d17d8cd8f4f13a73e752a80715337366c8f8f5cbb7d1f1680c6b1289",
        "CLIENT",
    ),
)
