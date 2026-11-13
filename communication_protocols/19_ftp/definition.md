# FTP — File Transfer Protocol

## ¿Qué es?

Un protocolo de aplicación para transferir archivos entre cliente y servidor.

## ¿Cómo funciona y para qué sirve?

Mantiene una conexión de control, normalmente en el puerto **21**, y conexiones
separadas para transferir datos. Los modos activo y pasivo determinan cómo se
establecen esas conexiones. Permite subir, descargar y listar archivos.

## Ideas clave

- FTP clásico no cifra credenciales ni contenido.
- FTPS añade protección TLS a FTP y requiere una configuración compatible.
- SFTP es otro protocolo, basado en SSH; no es FTP con una opción de seguridad.
- Las conexiones de datos adicionales pueden complicar firewalls y NAT.
- Para nuevas transferencias sensibles conviene evaluar SFTP, FTPS o HTTPS.

**Referencia:** [RFC 959](https://www.rfc-editor.org/rfc/rfc959.html).
