# ARP — Address Resolution Protocol

## ¿Qué es?

El protocolo que permite conocer la dirección MAC asociada a una dirección IPv4
en una red local.

## ¿Cómo funciona y para qué sirve?

Un equipo pregunta qué dispositivo tiene cierta IPv4. El propietario responde
con su MAC y el resultado se guarda temporalmente en una caché.
Para un destino de otra red se busca la MAC del siguiente salto, normalmente
el router, no la del servidor remoto.

## Ideas clave

- ARP trabaja dentro del enlace local; no resuelve nombres de dominio.
- IPv6 utiliza Neighbor Discovery, basado en ICMPv6, en lugar de ARP.
- ARP no autentica las respuestas; una red sin protecciones puede sufrir suplantación.

**Referencia:** [RFC 826](https://www.rfc-editor.org/rfc/rfc826.html).
