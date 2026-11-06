# Tema: configurar la firma y el vencimiento de los tokens.
import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent


def load_config() -> dict:
    load_dotenv(ROOT / ".env")
    return {
        "SERVICE_NAME": "onb-msa-sp-auth",
        "JWT_PRIVATE_KEY_FILE": os.getenv(
            "JWT_PRIVATE_KEY_FILE", str(ROOT.parent / ".secrets/jwt-private.pem")
        ),
        "JWT_ISSUER": os.getenv("JWT_ISSUER", "coe-auth"),
        "JWT_AUDIENCE": os.getenv("JWT_AUDIENCE", "coe-backend"),
        "JWT_ACCESS_TTL": int(os.getenv("JWT_ACCESS_TTL", "900")),
    }
