# WebSocket

## ¿Qué es?

Un protocolo de aplicación que mantiene una conexión bidireccional: cliente y
servidor pueden enviar mensajes sin una solicitud HTTP nueva por cada mensaje.

## ¿Cómo funciona y para qué sirve?

En su establecimiento clásico, una negociación HTTP cambia la conexión a WebSocket.
Después se intercambian mensajes de texto o binarios. Sirve para chats,
notificaciones y actualización de estados de pedidos.

## Ideas clave

- `ws` identifica conexiones sin TLS y `wss`, conexiones protegidas.
- A diferencia del polling, el servidor puede enviar una actualización cuando ocurre.
- Es necesario gestionar autenticación, permisos, desconexiones y reconexiones.
- No proporciona por sí solo historial, persistencia ni recuperación de mensajes perdidos.
- Mantener conexiones abiertas consume recursos del servidor.

**Referencia:** [RFC 6455](https://www.rfc-editor.org/rfc/rfc6455.html).
