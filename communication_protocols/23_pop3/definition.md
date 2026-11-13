# POP3 — Post Office Protocol, versión 3

## ¿Qué es?

Un protocolo para recuperar mensajes de un buzón de correo y descargarlos
al cliente.

## ¿Cómo funciona y para qué sirve?

El cliente se autentica, consulta los mensajes y los descarga. Puede marcar
mensajes para eliminarlos del servidor; conservar copias depende de la
configuración del cliente y del servidor.

## Ideas clave

- Su enfoque es descargar correo; no ofrece la sincronización de carpetas y
  estados entre dispositivos propia de IMAP.
- Puertos habituales: **110**, con posibilidad de STLS, y **995**, con TLS implícito.
- No envía mensajes: para eso se utiliza SMTP.
- Puede servir para recuperación sencilla; IMAP suele encajar mejor con varios dispositivos.
- Descargar un mensaje no obliga a eliminar su copia del servidor.

**Referencia:** [RFC 1939](https://www.rfc-editor.org/rfc/rfc1939.html).
