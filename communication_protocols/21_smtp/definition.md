# SMTP — Simple Mail Transfer Protocol

## ¿Qué es?

El protocolo utilizado para enviar y retransmitir correo electrónico.

## ¿Cómo funciona y para qué sirve?

Un cliente entrega el mensaje a un servidor de correo. Este puede consultar los
registros MX del dominio destinatario y transferirlo a otro servidor hasta
depositarlo en el sistema de correo receptor.

## Ideas clave

- Puertos habituales: **25** para transferencia entre servidores, **587** para
  envío autenticado y **465** para envío con TLS implícito.
- SMTP envía correo; IMAP y POP3 permiten acceder al correo recibido.
- Aceptar un mensaje no garantiza que llegue a la bandeja de entrada.
- TLS protege una conexión; no equivale a cifrado del mensaje de extremo a extremo.
- SPF, DKIM y DMARC ayudan a combatir la suplantación de dominios.

**Referencia:** [RFC 5321](https://www.rfc-editor.org/rfc/rfc5321.html).
