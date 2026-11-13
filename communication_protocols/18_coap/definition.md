# CoAP — Constrained Application Protocol

## ¿Qué es?

Un protocolo de aplicación para dispositivos y redes con recursos limitados.
Utiliza recursos y operaciones similares a las de HTTP, con mensajes compactos.

## ¿Cómo funciona y para qué sirve?

Un cliente consulta o modifica un recurso de un dispositivo mediante operaciones
como GET, POST, PUT y DELETE. Su especificación base utiliza UDP y permite mensajes
confirmables con retransmisión o mensajes no confirmables.

## Ideas clave

- Se utiliza en sensores, automatización y sistemas IoT.
- Es diferente de MQTT: su base es solicitud/respuesta, no publicación mediante broker.
- Puede protegerse con DTLS; existen otras extensiones de transporte y seguridad.
- Puertos habituales: **5683** y **5684** con DTLS.
- Menor tamaño de mensaje no elimina pérdidas ni restricciones de la red.

**Referencia:** [RFC 7252](https://www.rfc-editor.org/rfc/rfc7252.html).
