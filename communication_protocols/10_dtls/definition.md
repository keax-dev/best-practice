# DTLS — Datagram Transport Layer Security

## ¿Qué es?

Un protocolo que adapta la protección de TLS a transportes de datagramas,
habitualmente UDP.

## ¿Cómo funciona y para qué sirve?

Establece claves y protege la confidencialidad e integridad de los mensajes.
Su negociación contempla pérdidas y desorden, propios de una red de datagramas.
Se utiliza en aplicaciones de tiempo real e IoT, por ejemplo para proteger CoAP.

## Ideas clave

- Protege mensajes sin convertir UDP en un flujo como TCP.
- No garantiza que todos los datos de la aplicación lleguen ni que lleguen ordenados.
- Las necesidades de retransmisión de negocio siguen dependiendo del protocolo superior.
- DTLS y TLS están relacionados, pero no son intercambiables directamente.

**Referencia:** [DTLS 1.3: RFC 9147](https://www.rfc-editor.org/rfc/rfc9147.html).
