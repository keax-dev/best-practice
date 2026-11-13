# HTTP — Hypertext Transfer Protocol

## ¿Qué es?

Un protocolo de aplicación basado en solicitudes y respuestas. Se utiliza para
consultar páginas, archivos y APIs.

## ¿Cómo funciona y para qué sirve?

El cliente envía método, destino, encabezados y, opcionalmente, un cuerpo.
El servidor responde con un código de estado, encabezados y, cuando corresponde,
un cuerpo. Ejemplo: consultar `/orders` y recibir un listado JSON.

## Ideas clave

- Métodos: **GET** consulta, **POST** procesa o crea, **PUT** reemplaza,
  **PATCH** modifica parcialmente y **DELETE** solicita eliminar.
- Estados: **2xx** éxito, **3xx** redirección, **4xx** error del cliente, **5xx** error del servidor.
- Es sin estado: cada solicitud debe poder interpretarse por sí misma.
- HTTP/1.1 y HTTP/2 utilizan TCP; HTTP/3 utiliza QUIC.
- REST es un estilo de diseño que suele apoyarse en HTTP; JSON es un formato de datos.

**Referencia:** [Semántica HTTP: RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html).
