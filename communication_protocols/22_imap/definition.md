# IMAP — Internet Message Access Protocol

## ¿Qué es?

Un protocolo para consultar y administrar el correo almacenado en un servidor.

## ¿Cómo funciona y para qué sirve?

El cliente sincroniza mensajes, carpetas e indicadores como leído o no leído.
El servidor mantiene el estado del buzón, lo que permite acceder desde varios
dispositivos. Los clientes también pueden conservar copias locales.

## Ideas clave

- Se utiliza para leer y organizar correo; el envío corresponde a SMTP.
- Puertos habituales: **143**, con posibilidad de STARTTLS, y **993**, con TLS implícito.
- Facilita mantener una vista coherente del buzón entre móvil y computador.
- Borrar o mover mensajes puede afectar lo que ven los otros dispositivos.
- Deben utilizarse conexiones protegidas y autenticación adecuada.

**Referencia:** [IMAP4rev2: RFC 9051](https://www.rfc-editor.org/rfc/rfc9051.html).
