# QUIC

## ¿Qué es?

Un protocolo de transporte seguro que funciona sobre UDP. Proporciona conexiones
con múltiples flujos y es la base de HTTP/3.

## ¿Cómo funciona y para qué sirve?

Integra TLS 1.3, confirmaciones, recuperación de pérdidas y control de congestión.
Permite que varios flujos avancen de manera independiente dentro de una conexión.
Se utiliza para mejorar comunicaciones web y admitir cambios de ruta de red.

## Ideas clave

- Usar UDP como base no significa renunciar a fiabilidad ni cifrado.
- La pérdida de datos de un flujo no obliga a detener la entrega de otros flujos.
- Puede mantener una conexión cuando cambia la dirección de red del cliente.
- QUIC es transporte; HTTP/3 es un protocolo de aplicación que lo utiliza.

**Referencia:** [RFC 9000](https://www.rfc-editor.org/rfc/rfc9000.html).
