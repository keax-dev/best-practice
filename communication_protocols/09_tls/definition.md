# TLS — Transport Layer Security

## ¿Qué es?

Un protocolo que protege una comunicación mediante cifrado, comprobación de
integridad y autenticación del extremo remoto.

## ¿Cómo funciona y para qué sirve?

Durante el establecimiento de la sesión, las partes negocian parámetros de
seguridad y claves. En el uso web habitual, el cliente verifica el certificado
del servidor y que corresponda al nombre solicitado. Después intercambian datos cifrados.

## Ideas clave

- Se utiliza para proteger HTTP, correo y otras comunicaciones.
- La autenticación mediante certificados de ambos extremos se conoce como **mTLS**.
- No sustituye el login, JWT ni los permisos de la aplicación.
- Desactivar la verificación del certificado permite suplantar al servidor.
- TLS 1.3 es una versión moderna; SSL es un antecedente obsoleto.

**Referencia:** [TLS 1.3: RFC 8446](https://www.rfc-editor.org/rfc/rfc8446.html).
