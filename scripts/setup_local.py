# Tema: generar claves locales sin sobrescribir secretos existentes.
import argparse
import secrets
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

ROOT = Path(__file__).resolve().parents[1]


def prepare(directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    private_path = directory / "jwt-private.pem"
    public_path = directory / "jwt-public.pem"
    if private_path.exists():
        private_key = serialization.load_pem_private_key(
            private_path.read_bytes(), password=None
        )
    else:
        if public_path.exists():
            raise ValueError("Public key exists without its private key")
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        with private_path.open("xb") as file:
            file.write(
                private_key.private_bytes(
                    serialization.Encoding.PEM,
                    serialization.PrivateFormat.PKCS8,
                    serialization.NoEncryption(),
                )
            )
        private_path.chmod(0o600)
    if not isinstance(private_key, rsa.RSAPrivateKey):
        raise TypeError("The key must be RSA")
    public_bytes = private_key.public_key().public_bytes(
        serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo
    )
    if public_path.exists():
        if public_path.read_bytes() != public_bytes:
            raise ValueError("Public and private keys do not match")
    else:
        with public_path.open("xb") as file:
            file.write(public_bytes)
    for name in ("internal-api.key", "orders-service.key"):
        path = directory / name
        if not path.exists():
            with path.open("x", encoding="utf-8") as file:
                file.write(secrets.token_urlsafe(48))
            path.chmod(0o600)
        if len(path.read_text(encoding="utf-8").strip()) < 32:
            raise ValueError(f"{name} must contain at least 32 characters")
    print(f"Local keys ready: {directory}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Preparar las claves de la práctica local"
    )
    parser.add_argument("--directory", type=Path, default=ROOT / ".secrets")
    prepare(parser.parse_args().directory.resolve())
