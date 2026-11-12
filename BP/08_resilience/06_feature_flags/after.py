# Tema: un proveedor explícito permite activar o desactivar el comportamiento.
from dataclasses import dataclass


@dataclass
class FeatureFlags:
    new_checkout: bool = False


def checkout_label(flags: FeatureFlags) -> str:
    return "New checkout" if flags.new_checkout else "Classic checkout"


if __name__ == "__main__":
    flags = FeatureFlags()
    print(checkout_label(flags))
    flags.new_checkout = True
    print(checkout_label(flags))
