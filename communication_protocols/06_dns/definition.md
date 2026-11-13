# DNS — Domain Name System

## ¿Qué es?

Un sistema distribuido de nombres y su protocolo de consulta. Permite buscar
datos asociados a dominios, como las direcciones de `api.example.com`.

## ¿Cómo funciona y para qué sirve?

El cliente consulta un resolvedor. Si no tiene una respuesta en caché, este puede
consultar la jerarquía DNS hasta obtenerla. El TTL indica cuánto tiempo puede
conservarse un registro en caché.

## Ideas clave

- Registros habituales: **A** (IPv4), **AAAA** (IPv6), **CNAME** (alias), **MX** (correo).
- DNS clásico utiliza UDP y TCP, normalmente en el puerto 53.
- DNS sobre TLS o HTTPS cifra la comunicación con el resolvedor.
- DNSSEC permite verificar autenticidad e integridad de datos firmados; no los cifra.

**Referencia:** [RFC 1034](https://www.rfc-editor.org/rfc/rfc1034.html).
