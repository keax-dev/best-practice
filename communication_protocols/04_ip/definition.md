# IP — Internet Protocol

## ¿Qué es?

El protocolo que permite direccionar y transportar paquetes entre redes.
Sus versiones principales son IPv4, con direcciones de 32 bits, e IPv6, de 128 bits.

## ¿Cómo funciona y para qué sirve?

Cada paquete contiene direcciones de origen y destino. Los routers consultan
sus tablas de rutas para enviarlo hacia el siguiente salto hasta llegar al destino.

## Ideas clave

- IP ofrece entrega de mejor esfuerzo: puede haber pérdida, duplicación o desorden.
- Los puertos pertenecen a protocolos como TCP y UDP, no a IP.
- Una IP privada se utiliza dentro de redes privadas; no es directamente enrutable
  desde internet. NAT puede traducir direcciones, pero no sustituye un firewall.
- IP no cifra por sí solo el contenido de una aplicación.

**Referencia:** [IPv6: RFC 8200](https://www.rfc-editor.org/rfc/rfc8200.html).
