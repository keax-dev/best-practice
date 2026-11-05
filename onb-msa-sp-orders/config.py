# Tema: configuración explícita mediante variables de entorno.
import math
import os
from pathlib import Path
from urllib.parse import urlsplit

from dotenv import load_dotenv


def positive_timeout(name: str, default: str) -> float:
    value = float(os.getenv(name, default))
    if not math.isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be finite and positive")
    return value


def service_url(name: str, default: str) -> str:
    value = os.getenv(name, default).rstrip("/")
    parsed = urlsplit(value)
    if (
        parsed.scheme not in {"http", "https"}
        or not parsed.hostname
        or parsed.path
        or parsed.query
        or parsed.fragment
        or parsed.username
        or parsed.password
    ):
        raise ValueError(f"{name} must be an HTTP origin without path or credentials")
    return value


def load_config() -> dict:
    load_dotenv(Path(__file__).parent / ".env")
    settings = {"SERVICE_NAME": "onb-msa-sp-orders", "JSON_SORT_KEYS": False}
    settings.update(
        API_GATEWAY_URL=service_url("API_GATEWAY_URL", "http://127.0.0.1:5000"),
        CONNECT_TIMEOUT=positive_timeout("CONNECT_TIMEOUT", "1"),
        VALIDATION_TIMEOUT=positive_timeout("VALIDATION_TIMEOUT", "5"),
    )
    return settings
