# Tema: transporte HTTP sin reglas de negocio ni persistencia.
from urllib.parse import urlsplit

import requests
from flask import Response, request

from api.errors import BusinessError

HOP_HEADERS = {
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "proxy-connection",
    "te",
    "trailer",
    "transfer-encoding",
    "upgrade",
    "host",
    "content-length",
}


def clean_headers(headers, *, decoded: bool = False) -> dict[str, str]:
    blocked = HOP_HEADERS | {
        name.strip().lower() for name in headers.get("Connection", "").split(",")
    }
    if decoded:
        # requests descomprime el cuerpo recibido: no conservar Content-Encoding.
        blocked |= {"content-encoding"}
    return {key: value for key, value in headers.items() if key.lower() not in blocked}


class ProxyHTTPClient:
    def __init__(
        self,
        destinations: dict[str, str],
        connect_timeout: float,
        orders_timeout: float,
        inventories_timeout: float,
    ) -> None:
        self.destinations = destinations
        self.connect_timeout = connect_timeout
        self.timeouts = {"orders": orders_timeout, "inventories": inventories_timeout}

    def forward(self, resource: str) -> Response:
        destination = self.destinations[resource]
        # Un salto solo puede reenviarse una vez a cada destino.
        visited = request.headers.get("X-Gateway-Route", "").split(",")
        target = urlsplit(destination)
        incoming = urlsplit(request.host_url)
        if resource in visited or (target.hostname, target.port) == (
            incoming.hostname,
            incoming.port,
        ):
            raise BusinessError(
                "SERVICE_UNAVAILABLE", "Bucle de enrutamiento bloqueado", 502
            )
        headers = clean_headers(request.headers)
        headers["X-Gateway-Route"] = ",".join(
            [part for part in visited if part] + [resource]
        )
        try:
            response = requests.request(
                request.method,
                destination + request.path,
                params=list(request.args.items(multi=True)),
                data=request.get_data(),
                headers=headers,
                timeout=(self.connect_timeout, self.timeouts[resource]),
                allow_redirects=False,
            )
        except requests.Timeout as error:
            raise BusinessError(
                "UPSTREAM_TIMEOUT", "Tiempo de espera agotado", 504
            ) from error
        except requests.RequestException as error:
            raise BusinessError(
                "SERVICE_UNAVAILABLE", "Servicio no disponible", 502
            ) from error
        if response.status_code in (502, 504):
            raise BusinessError(
                "INVALID_RESPONSE", "Respuesta inválida del servicio", 502
            )
        return Response(
            response.content,
            status=response.status_code,
            headers=clean_headers(response.headers, decoded=True),
        )
