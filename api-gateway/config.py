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
    settings = {"SERVICE_NAME": "api-gateway", "JSON_SORT_KEYS": False}
    settings.update(
        AUTH_SERVICE_URL=service_url("AUTH_SERVICE_URL", "http://127.0.0.1:5003"),
        AUTH_TIMEOUT=positive_timeout("AUTH_TIMEOUT", "3"),
        ORDERS_SERVICE_URL=service_url("ORDERS_SERVICE_URL", "http://127.0.0.1:5001"),
        INVENTORIES_SERVICE_URL=service_url(
            "INVENTORIES_SERVICE_URL", "http://127.0.0.1:5002"
        ),
        CONNECT_TIMEOUT=positive_timeout("CONNECT_TIMEOUT", "1"),
        ORDERS_TIMEOUT=positive_timeout("ORDERS_TIMEOUT", "10"),
        INVENTORIES_TIMEOUT=positive_timeout("INVENTORIES_TIMEOUT", "2"),
    )
    if (
        len(
            {
                settings["ORDERS_SERVICE_URL"],
                settings["INVENTORIES_SERVICE_URL"],
                settings["AUTH_SERVICE_URL"],
            }
        )
        != 3
    ):
        raise ValueError("Destinations must be different")
    if (
        settings["ORDERS_TIMEOUT"]
        <= settings["INVENTORIES_TIMEOUT"] + 2 * settings["CONNECT_TIMEOUT"]
    ):
        raise ValueError("ORDERS_TIMEOUT must allow time for the inner validation")
    return settings
