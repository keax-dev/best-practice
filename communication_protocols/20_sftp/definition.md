# SFTP — SSH File Transfer Protocol

## ¿Qué es?

Un protocolo de transferencia y administración de archivos que normalmente
funciona como un subsistema de SSH.

## ¿Cómo funciona y para qué sirve?

El cliente establece una conexión SSH, verifica la identidad del servidor y se
autentica. Después puede listar, subir, descargar o modificar archivos dentro de
los permisos concedidos. Es habitual en intercambios automatizados entre sistemas.

## Ideas clave

- Usa normalmente el puerto **22** y aprovecha el cifrado de SSH.
- Puede autenticarse mediante claves públicas o contraseñas, según configuración.
- Hay que verificar la clave del servidor para evitar suplantaciones.
- Es distinto de FTP y FTPS; sus clientes no son intercambiables directamente.
- Deben limitarse los directorios y permisos de las cuentas de transferencia.

**Referencia:** [Manual oficial de OpenSSH: sftp](https://man.openbsd.org/sftp).
