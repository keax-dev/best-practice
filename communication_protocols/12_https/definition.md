# HTTPS — HTTP con una conexión segura

## ¿Qué es?

El uso de HTTP sobre una comunicación protegida mediante TLS. Conserva los
métodos y estados de HTTP, añadiendo protección durante el transporte.

## ¿Cómo funciona y para qué sirve?

El cliente verifica la identidad del servidor y establece una conexión cifrada
antes de intercambiar información HTTP. Se utiliza en sitios web y APIs,
especialmente cuando viajan contraseñas, tokens o datos personales.

## Ideas clave

- Usa normalmente el puerto **443**.
- Protege confidencialidad e integridad; no garantiza que el sitio sea honesto.
- No reemplaza autorización, validación de entradas ni protección de datos almacenados.
- En un gateway, la conexión hacia cada servicio requiere su propia protección.
- En HTTP/3, QUIC integra la negociación de seguridad con TLS 1.3.

**Referencia:** [Esquema HTTPS: RFC 9110, sección 4.2.2](https://www.rfc-editor.org/rfc/rfc9110.html#section-4.2.2).
