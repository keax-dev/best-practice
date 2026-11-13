# TCP — Transmission Control Protocol

## ¿Qué es?

Un protocolo de transporte orientado a conexión que ofrece un flujo de bytes
fiable y ordenado entre dos extremos.

## ¿Cómo funciona y para qué sirve?

Establece una conexión, numera datos, confirma su recepción y retransmite pérdidas.
También regula el flujo y la congestión. Se usa en HTTP/1.1, HTTP/2, correo y SSH.

## Ideas clave

- No conserva límites de mensajes: una lectura puede contener parte de un mensaje
  o varios. La aplicación necesita definir cómo separarlos.
- Una conexión puede fallar; la aplicación debe manejar errores y timeouts.
- Confirmar bytes no significa que una operación de negocio se haya completado.
- TCP no cifra la información; puede combinarse con TLS.

**Referencia:** [RFC 9293](https://www.rfc-editor.org/rfc/rfc9293.html).
