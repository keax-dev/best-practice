# Tema: recibir una credencial y evitar exponerla en resultados o representaciones.
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Credentials:
    token: str = field(repr=False)


def load_credentials(values: dict[str, str]) -> Credentials:
    token = values.get("APP_ACCESS_TOKEN", "").strip()
    if not token:
        raise ValueError("APP_ACCESS_TOKEN is required")
    return Credentials(token)


if __name__ == "__main__":
    # Este valor es una entrada simulada, no una credencial válida.
    credentials = load_credentials({"APP_ACCESS_TOKEN": "demo-only"})
    print(credentials)
    print("Credential loaded without exposing its value")
